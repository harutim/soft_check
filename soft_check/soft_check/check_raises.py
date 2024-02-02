"""
check_raises.py

This module provides utilities for checking exceptions raised during testing.

Functions:
- raises: A decorator to check if a specific exception is raised during the execution of a function.

Classes:
- CheckRaisesContext: A context manager to check if an exception is raised within a 'with' block.

Usage:
---------
Example 1: Using the 'raises' decorator

```python
from check_raises import raises

def test_function():
    with raises(ValueError):
        # Your test logic that should raise a ValueError

test_function()  # This will raise an AssertionError if a ValueError is not raised.

Example 2: Using the 'CheckRaisesContext' context manager

python
Copy code
from exception_utils import CheckRaisesContext

with CheckRaisesContext(ValueError, TypeError, custom_message="Either ValueError or TypeError was \
    expected."):
    # Your test logic that should raise a ValueError or TypeError

# This will raise an AssertionError if neither ValueError nor TypeError is raised within the 'with'\
 block.
"""
from .check_log import log_failure

_STOP_ON_FAIL = False


def raises(expected_exception, *args, **kwargs):
    """
    Decorator to check if a specific exception is raised.

    Args:
    - expected_exception (type or tuple): Expected exception type or a tuple of types.
    - *args: Positional arguments for the function to be decorated.
    - **kwargs: Keyword arguments for the function to be decorated, including 'msg' for a custom \
        message.

    Usage Example:
    ```python
    @raises(MyException, msg="Custom message")
    def my_function():
        # Your code that should raise MyException
    ```

    Returns:
    - None
    """
    __tracebackhide__ = True

    if isinstance(expected_exception, type):
        excepted_exceptions = (expected_exception,)
    else:
        excepted_exceptions = expected_exception

    assert all(
        isinstance(exc, type) or issubclass(exc, BaseException)
        for exc in excepted_exceptions
    )

    msg = kwargs.pop("msg", None)
    if not args:
        assert not kwargs, f"Unexpected kwargs for soft_check.raises: {kwargs}"
        return CheckRaisesContext(expected_exception, msg=msg)
    func = args[0]
    assert callable(func)
    with CheckRaisesContext(expected_exception, msg=msg):
        func(*args[1:], **kwargs)
    return None


class CheckRaisesContext:
    """
    Context manager to check if an exception is raised.

    Args:
    - expected_excs (tuple): Tuple of expected exception types.
    - msg (str): Custom message to log on failure.

    Usage Example:
    ```python
    with CheckRaisesContext(MyException, msg="Custom message"):
        # Your code that should raise MyException
    ```

    Global Variables:
    - _STOP_ON_FAIL (bool): Whether to stop on the first failure.

    Returns:
    - None
    """

    def __init__(self, *expected_excs, msg=None):
        """
        Initialize the context manager.

        Args:
        - expected_excs (tuple): Tuple of expected exception types.
        - msg (str): Custom message to log on failure.

        Returns:
        - None
        """
        self.expected_excs = expected_excs
        self.msg = msg

    def __enter__(self):
        """
        Enter the context.

        Returns:
        - CheckRaisesContext: The context manager instance.
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
        if exc_type is not None and issubclass(exc_type, self.expected_excs):
            return True

        if not _STOP_ON_FAIL:
            log_failure(self.msg if self.msg else exc_val)
            return True
        return False
