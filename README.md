# Retry Helper 

Helper tool fro retrying code when soem exceptions occur

## Usage

### RetryManager
Retry manager is context manager for retrying block of code. In fact its double layer context manager in first context you will create context manager and use while retry object is true. And the run you code in context of retry.attempt.

 * max_attempts - maximum count of attempts, default 1
 * wait_seconds - How many second it should wait before next retry, default 0
 * exceptions - exception class or tuple of exceptions classes which cause retry, if None all exceptions cause retry default None
 
```
with RetryManager(max_attempts=20, wait_seconds=1, exceptions=(TypeError,KeyError)) as retry:
while retry:
    with retry.attempt:
        # code raising exception if fail
```