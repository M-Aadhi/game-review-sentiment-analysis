"""
This module provides the core runtime for the model.
"""
import json
from enum import Enum
from dataclasses import dataclass
from logging import Logger
from typing import Optional
from ._exception import BaseError


@dataclass
class InvokeRequest:
    """
    Represents an invoke request object.

    Attributes:
        version (int): The version of the invoke request.
        protocol (str): The protocol used for the request.
        method (str): The HTTP method of the request.
        url (str): The path of the request.
        headers (dict): The headers of the request.
        body (str): The body of the request.
        is_base64_encoded (bool): Indicates if the body is base64 encoded.

    """
    version: int = 1
    protocol: Optional[str] = None
    method: Optional[str] = None
    url: Optional[str] = None
    headers: Optional[dict] = None
    body: Optional[str] = None
    is_base64_encoded: bool = False


@dataclass
class InvokeResponse:
    """
    Represents an invoke response object.

    Attributes:
        status_code (int): The status code of the response.
        headers (dict): The headers of the response.
        body (str): The body of the response.
        is_base64_encoded (bool): Indicates if the body is base64 encoded.

    """
    status_code: int = 200
    headers: Optional[dict] = None
    body: str = ''
    is_base64_encoded: bool = False

    def to_dict(self):
        """
        Converts the object to a dictionary representation.

        Returns:
            dict: A dictionary representing the object.
        """
        return {
            'statusCode': self.status_code,
            'headers': self.headers,
            'body': self.body,
            'isBase64Encoded': self.is_base64_encoded
        }

    def to_http_resp(self):
        """
        Converts the object to a dictionary representation.

        Returns:
            dict: A dictionary representing the object.
        """
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(self.to_dict()),
        }


@dataclass
class Args:
    """
    Represents the arguments passed to a function or method.

    Attributes:
        input (any): The parameters passed to the function or method.
        logger (Logger): The logger object used for logging.

    """
    input: object = None
    logger: Optional[Logger] = None


@dataclass
class ResponseBody:
    """
    Represents the response body of a function or method.

    Attributes:
        success (bool): Indicates if the function or method was successful.
        data (any): The data returned by the function or method.
        code (str): The code associated with the response.
        message (str): The message associated with the response.
    """
    data: Optional[str] = None
    code: Optional[str] = None
    message: Optional[str] = None

    def error(self, error: BaseError):
        """
        Sets the response body to an error response.

        Args:
            error (BaseError): The error object.
        """
        self.code = error.code
        self.message = error.message

    def to_json(self) -> str:
        """
        Converts the response body to a JSON string.

        Returns:
            str: The JSON string representation of the response body.
        """
        resp = {}
        if self.code != None and self.code != '':
            resp['code'] = self.code
            resp['message'] = self.message

        else:
            resp['data'] = self.data

        return json.dumps(resp)


class RunType(Enum):
    """
    Enum class for run types.

    Attributes:
        PROXY
        AWS
        VEFAAS
    """
    PROXY = 0,
    AWS = 1,
    VEFAAS = 2
