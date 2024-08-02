"""
This module provides the core runtime context variable.
"""
import contextvars
from . import _utils, _const

function_runtime_ctx = contextvars.ContextVar('function_runtime_ctx')


def get_ctx():
    """
    Get the context variable.
    """
    try:
        return function_runtime_ctx.get()
    except LookupError as e:
        return None


def set_ctx(ctx_var):
    """
    Set the context variable.
    """
    function_runtime_ctx.set(ctx_var)


def get_ctx_key(key):
    """
    Get the context variable by key.
    """
    ctx = get_ctx()
    if ctx is None:
        return None
    return get_ctx().get(key, None)


def add_ctx_key(key, value):
    """
    Add the context variable by key.
    """
    pre = get_ctx()
    pre[key] = value
    set_ctx(pre)


def init_stop_watch():
    """
    Init the stop watch.
    """
    stopwatch = _utils.Stopwatch()
    add_ctx_key(_const.CTX_KEY_STOPWATCH, stopwatch)


def init():
    """
    Init the context variable.
    """
    set_ctx({})
    init_stop_watch()


def get_stopwatch() -> _utils.Stopwatch:
    """
    Get the stop watch.
    """
    stopwatch = get_ctx_key(_const.CTX_KEY_STOPWATCH)
    return stopwatch


def set_request_id(value: str):
    """
    Set the request id.
    """
    add_ctx_key(_const.CTX_KEY_REQUEST_ID, value)


def get_request_id() -> str:
    """
    Get the request id.
    """
    return get_ctx_key(_const.CTX_KEY_REQUEST_ID)


def clear():
    """
    Clear the context variable.
    """
    function_runtime_ctx.set(None)
