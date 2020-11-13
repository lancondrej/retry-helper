import functools
import time



class RetryManager:
    """
    Retry context manager retrying block of code until success or max attempt occur
     success is when no exception was raised, you can specify what exception should be consider for retry

     It can be used also as decorator

    Args:
        max_attempts (int): maximum count of attempts, default 1
        wait_seconds (int): How many second it should wait before next retry, default 0
        exceptions (None, Exception, tuple): Exception class or tuple of exceptions class which cause retry, if None all exceptions cause retry default None

    Examples:
    with RetryManager(max_attempts=20, wait_seconds=1, exceptions=(TypeError,KeyError)) as retry:
    while retry:
        with retry.attempt:
            # code raising exception if fail

    @RetryManager(max_attempts=20, wait_seconds=1, exceptions=(TypeError,KeyError)) as retry:
    def my_function(*args, **kwargs):
        # my code
    """

    class Attempt:
        def __init__(self, retry_manager):
            self._retry_manager = retry_manager

        def __enter__(self):
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
                 exceptions: [None, Exception, tuple] = None) -> None:
        self.max_attempts = max_attempts
        self._attempt_count = 0
        self.wait_seconds = wait_seconds
        self._success = False
        self.attempt = RetryManager.Attempt(self)
        self.exceptions = exceptions

    def __enter__(self):
        self._attempt_count = 0
        self._success = False
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def succeeded(self):
        self._success = True

    def retry(self):
        self._attempt_count += 1

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
