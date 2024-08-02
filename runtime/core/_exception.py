"""
This module provides the core runtime exception.
"""
from enum import Enum


class ErrorCode(Enum):
    """
    Enum class for error codes.

    Attributes:
        ERR_SYSTEM_ERROR (str): System error.
        ERR_REQUEST_INVALID_BODY (str): Invalid request body.
        ERR_FUNCTION_NOT_FOUND (str): Function not found.
        ERR_FUNCTION_EXECUTION_ERROR (str): Function execution error.
    """
    ERR_SYSTEM_ERROR = "ERR_SYSTEM_ERROR"
    ERR_REQUEST_INVALID_BODY = "ERR_REQUEST_INVALID_BODY"
    ERR_FUNCTION_NOT_FOUND = "ERR_FUNCTION_NOT_FOUND"
    ERR_FUNCTION_EXECUTION_ERROR = "ERR_FUNCTION_EXECUTION_ERROR"


class BaseError(Exception):
    """
    Base class for custom exceptions.

    Attributes:
        code (str): The error code.
        message (str): The error message.
    """

    def __init__(self, code: str, message: str) -> None:
        """
            Initialize the Error object with the provided error message and code.

            Args:
                code (str): The error code.
                message (str): The error message.

            Returns:
                None

            Raises:
                None

        """
        super().__init__(f'Error: code: {code}, msg: {message}')
        self.code = code
        self.message = str(message)

    def to_json(self) -> dict:
        """
            Convert the object to a JSON-compatible dictionary.

            Returns:
                dict: A dictionary representation of the object.
                    The dictionary contains the following keys:
                    - 'code': The code value of the object.
                    - 'msg': The trimmed error message of the object.
        """
        return {
            'code': self.code,
            'message': self.message
        }


class RuntimeSystemError(BaseError):
    """
    Custom exception class for system errors.

    Attributes:
        code (str): The error code.
        message (str): The error message.
    """

    def __init__(self, message: str) -> None:
        super().__init__(ErrorCode.ERR_SYSTEM_ERROR.value, message)


class FunctionNotFoundError(BaseError):
    """
    Custom exception class for function not found errors.

    Attributes:
        code (str): The error code.
        message (str): The error message.
    """

    def __init__(self, message: str) -> None:
        super().__init__(ErrorCode.ERR_FUNCTION_NOT_FOUND.value, message)


class FunctionExecutionError(BaseError):
    """
    Custom exception class for function execution errors.

    Attributes:
        code (str): The error code.
        message (str): The error message.
    """

    def __init__(self, message: str) -> None:
        super().__init__(ErrorCode.ERR_FUNCTION_EXECUTION_ERROR.value, message)


class RequestInvalidBodyError(BaseError):
    """
    Custom exception class for invalid request body errors.

    Attributes:
        code (str): The error code.
        message (str): The error message.
    """

    def __init__(self, message: str) -> None:
        super().__init__(ErrorCode.ERR_REQUEST_INVALID_BODY.value, message)
