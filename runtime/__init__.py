from typing import TypeVar, Generic
from logging import Logger

T = TypeVar('T')

class Args(Generic[T]):
    input: T
    logger: Logger