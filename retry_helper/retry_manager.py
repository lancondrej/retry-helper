import functools
import time
import logging
from typing import Callable, Optional

logger = logging.getLogger(__name__)

class RetryManager:
    """
    Retry context manager retrying block of code until success or max attempt occur
     success is when no exception was raised, you can specify what exception should be consider for retry

     It can be used also as decorator

    Args:
        max_attempts (int): maximum count of attempts, default 1
        wait_seconds (int): How many second it should wait before next retry, default 0
        exceptions (None, Exception, tuple): Exception class or tuple of exceptions class which cause retry, if None all exceptions cause retry default None
        reset_func (None, Callable): function to be run before next retry

    Examples:
    with RetryManager(max_attempts=20, wait_seconds=1, exceptions=(TypeError,KeyError)) as retry:
    while retry:
        with retry.attempt:
            # code raising exception if fail

    @RetryManager(max_attempts=20, wait_seconds=1, exceptions=(TypeError,KeyError))
    def my_function(*args, **kwargs):
        # my code
    """

    class Attempt:
        def __init__(self, retry_manager):
            self._retry_manager = retry_manager

        def __enter__(self):
            if self._retry_manager.attempt_count != 0:
                self._retry_manager.reset()
            self._retry_manager.retry()
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type is None:
                self._retry_manager.succeeded()
                return bool(self._retry_manager)
            if not self._retry_manager.exceptions or issubclass(exc_type, self._retry_manager.exceptions):
                time.sleep(self._retry_manager.wait_seconds)
                return bool(self._retry_manager)

    def __init__(self, max_attempts: int = 1, wait_seconds: int = 0,
                 exceptions: [None, Exception, tuple] = None, reset_func: Optional[Callable] = None,
                 reset_func_kwargs: Optional[dict] = None) -> None:
        self.max_attempts = max_attempts
        self._attempt_count = 0
        self.wait_seconds = wait_seconds
        self._success = False
        self.attempt = RetryManager.Attempt(self)
        self.exceptions = exceptions
        self.reset_func = reset_func if callable(reset_func) else None
        self.reset_func_kwargs = reset_func_kwargs or {}

    def __enter__(self):
        self._attempt_count = 0
        self._success = False
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @property
    def attempt_count(self):
        return self._attempt_count

    def reset(self):
        if self.reset_func:
            logger.debug(f"Run reset func")
            self.reset_func(**self.reset_func_kwargs)

    def succeeded(self):
        logger.debug(f"Success on try number {self.attempt_count}")
        self._success = True

    def retry(self):
        self._attempt_count += 1
        logger.debug(f"Do try number {self.attempt_count}")

    def __bool__(self):
        return not self._success and self._attempt_count < self.max_attempts

    def __call__(self, func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            with self:
                while self:
                    with self.attempt:
                        return func(*args, **kwargs)

        return inner
