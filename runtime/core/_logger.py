"""
This module provides the core runtime for the logger.
"""
import logging
import json
from enum import Enum
from datetime import datetime, timezone
from . import _ctx, _const, _model

TRACE = 0
DEBUG = 1
INFO = 2
WARN = 3
ERROR = 4
FATAL = 5

log_level_map = {
    logging.NOTSET: TRACE,
    logging.DEBUG: DEBUG,
    logging.INFO: INFO,
    logging.WARNING: WARN,
    logging.ERROR: ERROR,
    logging.FATAL: FATAL,
    logging.CRITICAL: FATAL,
}


class LoggerType(Enum):
    """
    Enum class for logger types.

    Attributes:
        SYSTEM (int): System logger.
        USER (int): User logger.
    """
    SYSTEM = 0
    USER = 1


class LogFormatter(logging.Formatter):
    """
    RequestIdFormatter is a custom formatter that formats the request ID and API name.
    """
    run_type: _model.RunType
    logger_type: LoggerType

    def __init__(self, fmt, run_type: _model.RunType, logger_type: LoggerType):
        super().__init__(fmt)
        self.run_type = run_type
        self.logger_type = logger_type

    def format(self, record):
        try:
            record.message = record.getMessage()
        except Exception as e:
            record.message = '{}'.format(e)
        max_message_length = _const.MAX_MESSAGE_LENGTH
        if len(record.message) > max_message_length:
            limit_message = '\n... The log has been truncated because it exceeds the length limit ' + \
                str(max_message_length) + '.'
            record.message = record.message[:max_message_length] + \
                limit_message
        message = {
            'type': self.logger_type.value,
            'timestamp': int(datetime.now(timezone.utc).timestamp() * 1000),
            'level': log_level_map.get(record.levelno, 0),
            'content': record.message
        }
        request_id = _ctx.get_request_id()
        runtime_event = _ctx.get_ctx_key(_const.CTX_KEY_RUNTIME_EVENT)
        if runtime_event is not None:
            message.update(runtime_event)
        if request_id is not None:
            message.update({'request_id': request_id})
        record.message = json.dumps(message)

        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)
        s = self.formatMessage(record)
        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + record.exc_text
        if record.stack_info:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + self.formatStack(record.stack_info)
        return s


wrapper_json_fmt = '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": %(message)s}'

vefaas_json_fmt = '%(message)s'

proxy_logger_fmt = '%(message)s'


def create_formatter_logger(logger_type: LoggerType, run_type: _model.RunType) -> logging.Logger:
    """
    Create a logger with a JSON formatter.

    Args:
        logger_type (LoggerType): The type of logger to create.
        run_type (RunType): The type of run.

    Returns:
        logging.Logger: The logger.
    """

    logger = logging.getLogger(logger_type.name)
    fmt = proxy_logger_fmt
    if run_type == _model.RunType.PROXY:
        fmt = proxy_logger_fmt
        logger.setLevel(logging.DEBUG)
    elif run_type == _model.RunType.AWS:
        fmt = wrapper_json_fmt
        logger.setLevel(logging.INFO)
    elif run_type == _model.RunType.VEFAAS:
        fmt = vefaas_json_fmt
        logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(LogFormatter(fmt, run_type, logger_type))
    logger.addHandler(handler)
    return logger


sys_logger = None
user_logger = None


def init_logger(run_type: _model.RunType) -> None:
    """
    Initialize the logger.

    Args:
        run_type (RunType): The type of run.
    """
    global sys_logger, user_logger
    sys_logger = create_formatter_logger(LoggerType.SYSTEM, run_type)
    user_logger = create_formatter_logger(LoggerType.USER, run_type)


def get_sys_logger() -> logging.Logger:
    """
    Get the system logger.

    Returns:
        logging.Logger: The system logger.
    """
    return sys_logger


def get_user_logger() -> logging.Logger:
    """
    Get the user logger.

    Returns:
        logging.Logger: The user logger.
    """
    return user_logger
