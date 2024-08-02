"""
This module provides the core runtime for the utils.
"""
import time
import traceback
import sys
import importlib.util
from re import sub
from types import SimpleNamespace
from . import _const

FUNCTIONS_DIR_PATH = ''


# 设置函数的目录
def set_functions_dir_path(dir_path: str):
    """
    Set the functions directory path.

    Args:
        dir_path (str): The functions directory path.
    """
    global FUNCTIONS_DIR_PATH
    FUNCTIONS_DIR_PATH = dir_path


# 获取当前函数的目录
def get_function_path():
    """
    Get the current function path.

    Returns:
        str: The current function path.
    """
    return FUNCTIONS_DIR_PATH


def is_not_blank(s):
    """
    Check if the given string is not blank.

    Args:
        s (str): The string to check.

    Returns:
        bool: True if the string is not blank, False otherwise.
    """
    return bool(s and s.strip())


def time_delta_milliseconds(end_time, start_time):
    """
    Calculate the time difference in milliseconds between two given times.

    Args:
        end_time (float): The end time.
        start_time (float): The start time.

    Returns:
        int: The time difference in milliseconds.
    """
    return int((end_time - start_time) * 1000)


class Stopwatch:
    """
    A class for measuring the time elapsed between different events in a program.
    """
    project_init_time = time.time_ns()
    fn_init = 0
    is_project_first_invoke = True

    fn_start_time: int
    fn_load_start_time: int
    fn_run_start_time: int
    server_timing: dict
    x_runtime_timestamps: dict

    @staticmethod
    def project_init_start():
        """
        Start the project initialization time.
        """
        Stopwatch.project_init_time = time.time_ns()

    @staticmethod
    def project_init_end():
        """
        End the project initialization time.
        """
        Stopwatch.fn_init = time.time_ns() - Stopwatch.project_init_time

    def __init__(self) -> None:
        self.server_timing = {}
        self.x_runtime_timestamps = {}
        self.fn_start_time = time.time_ns()
        self.x_runtime_timestamps[_const.SERVER_TIMESTAMPS_KEY_REQUEST] = int(
            time.time_ns() / 1_000_000)

    def fn_load_start(self):
        """
        Start the function loading time.
        """
        self.fn_load_start_time = time.time_ns()

    def fn_load_end(self):
        """
        End the function loading time.
        """
        fn_load = time.time_ns() - self.fn_load_start_time
        self.server_timing[_const.SERVER_TIMING_KEY_FN_LOAD] = int(
            fn_load / 1_000_000)

    def fn_run_start(self):
        """
        Start the function execution time.
        """
        self.fn_run_start_time = time.time_ns()
        self.x_runtime_timestamps[_const.SERVER_TIMESTAMPS_KEY_USER_START] = int(
            time.time_ns() / 1_000_000)

    def fn_run_end(self):
        """
        End the function execution time.
        """
        fn_run = time.time_ns() - self.fn_run_start_time
        self.server_timing[_const.SERVER_TIMING_KEY_FN_RUN] = int(
            fn_run / 1_000_000)
        self.x_runtime_timestamps[_const.SERVER_TIMESTAMPS_KEY_USER_END] = int(
            time.time_ns() / 1_000_000)

    def fn_end(self):
        """
        End the function execution time.
        """
        fn_total = time.time_ns() - self.fn_start_time
        self.server_timing[_const.SERVER_TIMING_KEY_FN_TOTAL] = int(
            fn_total / 1_000_000)
        self.x_runtime_timestamps[_const.SERVER_TIMESTAMPS_KEY_RESPONSE] = int(
            time.time_ns() / 1_000_000)

    def to_time_headers(self):
        """
        Convert the stopwatch object to a dictionary of headers.

        Returns:
            dict: A dictionary of headers.
        """
        headers = {}
        if Stopwatch.is_project_first_invoke:
            self.server_timing[_const.SERVER_TIMING_KEY_FN_INIT] = int(
                Stopwatch.fn_init / 1_000_000)
            self.x_runtime_timestamps[_const.SERVER_TIMESTAMPS_KEY_INIT] = int(
                Stopwatch.project_init_time / 1_000_000)
            Stopwatch.is_project_first_invoke = False

        headers[_const.HTTP_HEADER_SERVER_TIMING] = ', '.join(
            [f'{key};dur={value}' for key, value in self.server_timing.items()])
        headers[_const.HTTP_HEADER_X_RUNTIME_TIMESTAMPS] = ', '.join(
            [f'{key}={value}' for key, value in self.x_runtime_timestamps.items()])
        return headers


def trim_err_msg(msg: str):
    """
    Trim the error message.

    Args:
        msg (str): The error message.

    Returns:
        str: The trimmed error message.
    """
    pattern = r' File ".*?/api/'
    return sub(pattern, '', msg)


def format_user_exception(limit=None):
    """
    Format the user exception.

    Args:
        limit (int, optional): The maximum number of lines to include in the exception message. Defaults to None.

    Returns:
        str: The formatted exception message.
    """
    exception_track = traceback.format_exception(*sys.exc_info())
    if limit is not None:
        exception_track = exception_track[limit:]
    return "".join(list(map(trim_err_msg, exception_track)))


class CustomNamespace(SimpleNamespace):
    def __getattr__(self, name):
        return self.__dict__.get(name, None)


def dict_to_namespace(d):
    """
    Convert a dictionary to a namespace object.

    Args:
        d (dict): The dictionary to convert.

    Returns:
        SimpleNamespace: The namespace object.
    """
    if isinstance(d, dict):
        return CustomNamespace(**{k: dict_to_namespace(v) for k, v in d.items()})
    elif isinstance(d, list):
        return [dict_to_namespace(item) for item in d]
    else:
        return d

def import_module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if (spec is None or spec.loader is None):
        raise Exception("File not found: " + file_path)
    real_module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = real_module
    spec.loader.exec_module(real_module)
    return real_module

