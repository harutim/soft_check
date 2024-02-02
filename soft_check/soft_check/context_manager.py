"""
Module Docstring:

This module provides a context manager for soft checks in pytest, along with related functions.

Usage Example:
```python
from soft_check import context_manager

with context_manager as c:
    # Your code that contains soft checks
    c.set_max_fail(5)  # Set max failures limit
    c.set_max_report(10)  # Set max reported failures limit
    c.set_max_tb(3)  # Set max traceback limit
Classes:

CheckContextManager: Context manager for soft checks in pytest.
Functions:

check_log.log_failure: Log a failure message.
Attributes:

_STOP_ON_FAIL (bool): Global variable to stop execution on failure (default: False).
"""
from . import check_log
from .check_log import log_failure

_STOP_ON_FAIL = False


class CheckContextManager:
    """
    Context manager for soft checks in pytest.

    Usage Example:
    ```python
    with CheckContextManager() as check:
        # Your code that contains soft checks
        check.set_max_fail(5)  # Set max failures limit
        check.set_max_report(10)  # Set max reported failures limit
        check.set_max_tb(3)  # Set max traceback limit
    ```

    Returns:
    - CheckContextManager: The context manager instance.
    """
    def __init__(self):
        """
        Initialize the context manager.

        Returns:
        - None
        """
        self.msg = None

    def __enter__(self):
        """
        Enter the context.

        Returns:
        - CheckContextManager: The context manager instance.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the context.

        Args:
        - exc_type (type): Type of the raised exception.
        - exc_val (Exception): The exception instance.
        - exc_tb (traceback): The traceback object.

        Returns:
        - bool: True if the exception matches the expected type, False otherwise.
        """
        __tracebackhide__ = True
        if exc_type is not None and issubclass(exc_type, AssertionError):
            if _STOP_ON_FAIL:
                self.msg = None
                return None
            if self.msg is not None:
                log_failure(f"{self.msg}\n{exc_val}")
            else:
                log_failure(exc_val)
            self.msg = None
            return True
        self.msg = None
        return None

    def __call__(self, msg=None):
        """
        Call the context manager with a custom message.

        Args:
        - msg (str): Custom message to log on failure.

        Returns:
        - CheckContextManager: The context manager instance.
        """
        self.msg = msg
        return self

    def set_max_fail(self, max_failures):
        """
        Set the maximum allowed failures.

        Args:
        - max_failures (int): Maximum allowed failures.

        Returns:
        - None
        """
        check_log._MAX_FAIL = max_failures

    def set_max_report(self, max_reported_failures):
        """
        Set the maximum allowed reported failures.

        Args:
        - max_reported_failures (int): Maximum allowed reported failures.

        Returns:
        - None
        """
        check_log._MAX_REPORT = max_reported_failures

    def set_max_tb(self, max_tb_limit):
        """
        Set the maximum allowed traceback limit.

        Args:
        - max_tb_limit (int): Maximum allowed traceback limit.

        Returns:
        - None
        """
        check_log._MAX_TB = max_tb_limit

check = CheckContextManager()
