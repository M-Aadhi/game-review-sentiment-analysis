"""
This module provides the core runtime const variable.
"""
PYTHON_LIB_NAME: str = 'packages'

API_DIR_NAME: str = 'api'

REQUEST_ID: str = 'requestId'

FILE_MANIFEST: str = 'manifest.json'

PATH_MANIFEST: str = '/__meta__/manifest.json'

HTTP_HEADER_SERVER_TIMING: str = 'x-runtime-timing'

HTTP_HEADER_X_RUNTIME_TIMESTAMPS: str = 'x-runtime-timestamps'

HTTP_HEADER_X_RUNTIME_REQUEST_ID: str = 'x-bizide-request-id'

HTTP_HEADER_X_RUNTIME_EVENT: str = 'x-runtime-event'

CTX_KEY_REQUEST_ID: str = 'request_id'

CTX_KEY_RUNTIME_EVENT: str = 'runtime_event'

CTX_KEY_STOPWATCH: str = 'stopwatch'

MANIFEST_KEY_API: str = 'api'

MANIFEST_KEY_ROUTE: str = 'route'

MANIFEST_KEY_FILE: str = 'file'

SERVER_TIMING_KEY_FN_LOAD: str = 'fn-load'

SERVER_TIMING_KEY_FN_RUN: str = 'fn-run'

SERVER_TIMING_KEY_FN_TOTAL: str = 'fn-total'

SERVER_TIMING_KEY_FN_INIT: str = 'fn-init'

SERVER_TIMESTAMPS_KEY_INIT: str = 'init'

SERVER_TIMESTAMPS_KEY_USER_START: str = 'user_start'

SERVER_TIMESTAMPS_KEY_USER_END: str = 'user_end'

SERVER_TIMESTAMPS_KEY_REQUEST: str = 'request'

SERVER_TIMESTAMPS_KEY_RESPONSE: str = 'response'

MAX_MESSAGE_LENGTH: int = 10 * 1024

MOUDLE_PREFIX = "__api__"
