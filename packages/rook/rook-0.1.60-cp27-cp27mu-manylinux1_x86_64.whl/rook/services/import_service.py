import sys
import traceback
import time
import threading
import types

import six
import os
import inspect
import site
import weakref
import imp

from collections import defaultdict

from rook.services.exts.cloud_debug_python.module_explorer import _GetLineNumbers
from six.moves import builtins

from rook.logger import logger

from rook.config import ImportServiceConfig

_SUPPORTED_PY_FORMATS = ['.py', '.pyc']


class CountingRLock(object):
    """
    Wraps threading.RLock() to make the recursion count visible.
    """
    def __init__(self):
        self._rlock = threading.RLock()
        self._count = 0

    def __enter__(self):
        lock = self._rlock.__enter__()
        self._count += 1
        return lock

    def __exit__(self, *args, **kwargs):
        self._count -= 1
        return self._rlock.__exit__(*args, **kwargs)

    def get_recursion_count(self):
        return self._count


class ImportLock(object):
    """
    When locked, only this thread can import (so all imports are guaranteed to have completed,
                                              and there are no partially initialized modules in sys.modules)
    """
    def __enter__(self):
        imp.acquire_lock()

    def __exit__(self, _, __, ___):
        imp.release_lock()


class ImportService(object):

    NAME = "Import"

    class Notification(object):
        def __init__(self, module_name, module_filename, include_externals, lineno, callback, code_object_callback, removed):
            self.module_name = module_name
            self.module_filename = module_filename
            self.callback = callback
            self.code_object_callback = code_object_callback
            self.removed = removed
            self.include_externals = include_externals
            self.lineno = lineno

    def __init__(self, bdb_location_service):
        self._bdb_location_service = bdb_location_service

        self._modules = dict(sys.modules)
        self._pickled_code_objects = defaultdict(list)
        self._post_import_notifications = {}
        self._lock = threading.RLock()

        self._thread = None
        self._quit = False

        self._old_import = None

        external_paths = [sys.exec_prefix]
        if hasattr(site, 'getsitepackages'):
            external_paths = external_paths + site.getsitepackages()

        self.external_paths = [os.path.normcase(os.path.realpath(external_path))
                               for external_path in external_paths]

        if ImportServiceConfig.USE_IMPORT_HOOK:
            import platform
            platform = platform.python_implementation().lower()

            def import_hook(*args, **kwargs):
                """
                Declared here to make it obvious that you can't replace the function by monkeypatching -
                the C extension will always reference the function set with SetImportHook.
                """
                __rookout__tracebackhide__ = True
                # this lock is here to keep us from checking imp.lock_held() after the root import handled by this
                # import hook call ends (so we expect the global import lock to be free),
                # but just after another thread started importing (so the global import lock is actually locked,
                # even though we want to evaluate as we're done imported _our_ root import).
                with import_hook.import_lock:
                    result = self._old_import(*args, **kwargs)

                    try:
                        # if the recursion count is > 1,
                        # then this call to import_hook is a nested import, which means that the parent
                        # import has not finished executing its code yet, but it's already in sys.modules.
                        # if we evaluate now, we will try to place BPs in the module before it finished executing,
                        # potentially resulting in CodeNotFound.
                        if import_hook.import_lock.get_recursion_count() == 1:
                            self.evaluate_module_list()
                    except:
                        pass

                    return result
            # this must be a reentrant lock - imports can cause other imports
            import_hook.import_lock = CountingRLock()

            if platform == "cpython":
                import native_extensions

                native_extensions.SetImportHook(import_hook)
                # atomic swap
                builtins.__import__, self._old_import = native_extensions.CallImportHookRemovingFrames, builtins.__import__
            elif platform == "pypy":
                import __pypy__
                # atomic swap
                builtins.__import__, self._old_import = __pypy__.hidden_applevel(import_hook), builtins.__import__
            else:
                # assertion should never be reached, singleton.py checks platform support
                raise AssertionError("Unsupported platform")
        else:
            self._thread = threading.Thread(target=self._query_thread,
                                            name=ImportServiceConfig.THREAD_NAME)
            self._thread.daemon = True
            self._thread.start()

    def close(self):
        if self._old_import:
            builtins.__import__ = self._old_import

        if self._thread:
            self._quit = True

            # If threading was monkey patched by gevent waiting on thread will likely throw an exception
            try:
                from gevent.monkey import is_module_patched
                if is_module_patched("threading"):
                    time.sleep(ImportServiceConfig.SYS_MODULES_QUERY_INTERVAL)
            except:
                pass

            self._thread.join()

    def register_post_import_notification(self, aug_id, name, filename, include_externals, lineno, callback, code_object_callback, removed):
        # Normalize file path
        if filename:
            filename = os.path.normcase(os.path.normpath(filename))

        notification = self.Notification(name, filename, include_externals, lineno, callback, code_object_callback, removed)

        with self._lock:
            # Attempt to satisfy notification using known modules
            for module_name, module_object in six.iteritems(self._modules):

                # Get module details and check if it matches
                module_filename = self._get_module_path(module_object)

                # If module is not valid, ignore
                if not self._is_valid_module(module_object, module_filename):
                    continue

                if module_filename:
                    found = False
                    if self._does_module_match_notification(module_name, module_filename, notification, self.external_paths):
                        notification.callback(module_object)
                        found = True

                    for filename, code_object_refs in self._pickled_code_objects.items():
                        if ImportService.path_contains_path(filename, notification.module_filename):
                            for code_object_ref in list(code_object_refs):  # list is copied to avoid races
                                code_object = code_object_ref()
                                if code_object is None:
                                    # code object has already been garbage collected,
                                    # but the pair still hasn't removed itself
                                    continue
                                if self._does_code_object_match_notification(code_object,
                                                                             notification):
                                    notification.code_object_callback(code_object, filename)
                            found = True
                    if found:
                        return False

            # Register notification for future loads
            self._post_import_notifications[aug_id] = notification

        return True

    def remove_aug(self, aug_id):
        with self._lock:
            try:
                notification = self._post_import_notifications[aug_id]
            except KeyError:
                return

            notification.removed()
            del self._post_import_notifications[aug_id]

    def clear_augs(self):
        with self._lock:
            for aug_id in list(self._post_import_notifications.keys()):
                self.remove_aug(aug_id)

            self._post_import_notifications.clear()

    def _is_valid_module(self, module_object, module_filename):
        return module_filename and os.path.splitext(module_filename)[1] in _SUPPORTED_PY_FORMATS and \
            module_object and inspect.ismodule(module_object) and hasattr(module_object, '__file__')

    def _query_thread(self):
        self._bdb_location_service.ignore_current_thread()

        while not self._quit:
            try:
                with ImportLock():
                    self.evaluate_module_list()
            except:
                if logger:
                    logger.exception("Error while evaluating module list")

            # time can be None if interpreter is in shutdown
            if not time:
                return
            time.sleep(ImportServiceConfig.SYS_MODULES_QUERY_INTERVAL)

    def evaluate_module_list(self):
        try:
            # Nobody is waiting for notifications
            if not self._post_import_notifications:
                return

            # No new modules
            if len(self._modules) == len(sys.modules):
                return

            with self._lock:

                # Get a fresh list
                modules = dict(sys.modules)

                # For everybody not in the old list, check notifications
                for name, module in six.iteritems(modules):
                    module_filename = self._get_module_path(module)
                    if name not in self._modules and self._is_valid_module(module, module_filename):
                        self._notify_of_new_module(module.__name__, module, module_filename)

                # Update the "old" list
                self._modules = modules

        except:
            logger.exception("Exception in ImportService")

    def _notify_of_pickled_code_object(self, module_name, filename, code_object):
        with self._lock:
            self._pickled_code_objects[filename].append(weakref.ref(code_object,
                                                                    lambda deadref:
                                                                    self._pickled_code_objects[filename].remove(deadref)))

            self.evaluate_module_list()
            self._trigger_all_notifications_for_module(filename, module_name, code_object)

    def _notify_of_new_module(self, module_name, module_object, module_filename):
        self._trigger_all_notifications_for_module(module_filename, module_name, module_object)

    def _trigger_all_notifications_for_module(self, module_filename, module_name, module_object_or_code_object):
        augs_to_remove = set()

        if module_filename:
            for aug_id, notification in six.iteritems(self._post_import_notifications.copy()):
                if self._does_module_match_notification(module_name, module_filename, notification,
                                                        self.external_paths):
                    try:
                        if isinstance(module_object_or_code_object, types.ModuleType):
                            augs_to_remove.add(aug_id)
                            notification.callback(module_object_or_code_object)
                        elif isinstance(module_object_or_code_object, types.CodeType):
                            if self._does_code_object_match_notification(module_object_or_code_object, notification):
                                augs_to_remove.add(aug_id)
                                notification.code_object_callback(module_object_or_code_object, module_filename)
                        else:
                            raise KeyError(type(module_object_or_code_object))
                    except:
                        logger.exception("Error on module load callback")
        for aug_id in augs_to_remove:
            self._post_import_notifications.pop(aug_id, None)

    @staticmethod
    def _get_module_path(module):
        try:
            path = inspect.getsourcefile(module)
        except:
            return None

        if path:
            return os.path.normcase(os.path.abspath(path))

        return None


    @staticmethod
    def _does_module_match_notification(module_name, module_filename, notification, external_paths):
        if not notification.include_externals:
            for external_path in external_paths:
                if module_filename.startswith(external_path):
                    return False

        if notification.module_filename and ImportService.path_contains_path(module_filename, notification.module_filename) or \
                        notification.module_name and module_name == notification.module_name:
            return True
        else:
            return False

    @staticmethod
    def _does_code_object_match_notification(code_object, notification):
        return notification.lineno in _GetLineNumbers(code_object)

    @staticmethod
    def path_contains_path(full_path, partial_path):
        if full_path.endswith(partial_path):
            return len(full_path) == len(partial_path) or full_path[-len(partial_path)-1] in ('/', '\\')
        else:
            return False
