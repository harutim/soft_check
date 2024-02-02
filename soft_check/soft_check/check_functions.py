"""
check_functions.py: A module providing soft check assertion functions.

This module contains a collection of assertion functions that can be used
to enhance the expressiveness and readability of tests. These functions are
designed to be used with testing frameworks like PyTest.

Usage:
1. Import this module into your test script.
2. Use the provided assertion functions in your test cases.

Example:
```python
import soft_check as check

def test_example():
    result = perform_some_operation()
    check.assert_equal(first_value, second_value, "first_value should be equal to second_value")
    check.not_equal(first_value, second_value, "first_value should not be equal to second_value")

Available Assertion Functions:

- check_func(func): Decorator function for checking the validity of another function.
- assert_equal(first_value, second_value, msg=""): Check if two values are equal and raise an \
    AssertionError if they are not.
- equal(first_value, second_value, msg=""): Compare two values for equality.
- not_equal(first_value, second_value, msg=""): Compare two values for inequality.
- is_(first_value, second_value, msg=""): Check if two values refer to the same object.
- is_not(first_value, second_value, msg=""): Check if two values do not refer to the same object.
- is_true(value, msg=""): Check if a given value evaluates to True.
- is_false(value, msg=""): Check if a given value evaluates to False.
- is_none(value, msg=""): Check if a given value is None.
- is_not_none(value, msg=""): Check if a given value is not None.
- is_in(value, iterable, msg=""): Check if a value is present in a given iterable.
- is_not_in(value, iterable, msg=""): Check if a value is not present in a given iterable.
- is_instance(value, type_to_check, msg=""): Check if a value is an instance of a specified type.
- is_not_instance(value, type_to_check, msg=""): Check if a value is not an instance of a specified\
      type.
- almost_equal(first_value, second_value, rel=None, abs_tol=None, msg=""): Check if two values are \
    almost equal within the specified relative and absolute tolerances.
- not_almost_equal(first_value, second_value, rel=None, abs_tol=None, msg=""): Check if two values \
    are not almost equal within the specified relative and absolute tolerances.
- greater(first_value, second_value, msg=""): Check if the first value is greater than the second.
- greater_equal(first_value, second_value, msg=""): Check if the first value is greater than or \
    equal to the second.
- less(first_value, second_value, msg=""): Check if the first value is less than the second.
- less_equal(first_value, second_value, msg=""): Check if the first value is less than or equal to \
    the second.
- between(value_to_check, lower_bound, upper_bound, msg="", lower_bound_included=False, \
    upper_bound_included=False): Check if a value is between two other values.

Note: Customize the messages (msg) for better error reporting.

For detailed information about each assertion function, refer to the function
docstrings within this module.
"""
import functools

import pytest

from .check_log import log_failure

__all__ = [
    "assert_equal",
    "equal",
    "not_equal",
    "is_",
    "is_not",
    "is_true",
    "is_false",
    "is_none",
    "is_not_none",
    "is_in",
    "is_not_in",
    "is_instance",
    "is_not_instance",
    "almost_equal",
    "not_almost_equal",
    "greater",
    "greater_equal",
    "less",
    "less_equal",
    "between",
    "check_func",
]


def check_func(func):
    """
    Decorator function for checking the validity of another function.

    This decorator catches AssertionError exceptions raised by the wrapped function
    and logs the failure using the log_failure function. If no exceptions occur,
    it returns True; otherwise, it returns False.

    Parameters:
    - func (callable): The function to be wrapped and checked.

    Returns:
    - wrapper (callable): The wrapper function that checks the validity of the input function.
                        Returns True if the function runs successfully, and False if an
                        AssertionError occurs.

    Example:
    python
    @check_func
    def example_function():
        assert 1 + 1 == 3
    """
    @functools.wraps(func)
    def wrapper(*args, **kwds):
        __tracebackhide__ = True
        try:
            func(*args, **kwds)
            return True
        except AssertionError as exc:
            log_failure(exc)
            return False

    return wrapper


def assert_equal(first_value, second_value, msg=""):
    """
    Check if two values are equal and raise an AssertionError if they are not.

    Parameters:
    - first_value: The first value for comparison.
    - second_value: The second value for comparison.
    - msg (optional): A custom error message to include in the AssertionError.

    Raises:
    - AssertionError: If `first_value` is not equal to `second_value`, an AssertionError is raised.
      If a custom message (`msg`) is provided, it will be included in the exception.

    Example:
    >>> assert_equal(3, 3, "Values should be equal")  # No exception is raised
    >>> assert_equal(3, 5, "Values should be equal")  # Raises AssertionError with the provided \
    message

    """
    assert first_value == second_value, msg


def equal(first_value, second_value, msg=""):
    """
    Compare two values for equality.

    Parameters:
    - first_value: The first value for comparison.
    - second_value: The second value for comparison.
    - msg (optional): A custom error message to include if the values are not equal.

    Returns:
    - bool: True if `first_value` is equal to `second_value`, False otherwise.

    Example:
    >>> equal(3, 3)  # Returns True
    >>> equal(3, 5, "Values should be equal")  # Returns False and logs a failure message

    """
    __tracebackhide__ = True
    if first_value == second_value:
        return True
    log_failure(f"check {first_value} == {second_value}", msg)
    return False


def not_equal(first_value, second_value, msg=""):
    """
    Compare two values for inequality.

    Parameters:
    - first_value: The first value for comparison.
    - second_value: The second value for comparison.
    - msg (optional): A custom error message to include if the values are equal.

    Returns:
    - bool: True if `first_value` is not equal to `second_value`, False otherwise.

    Example:
    >>> not_equal(3, 5)  # Returns True
    >>> not_equal(3, 3, "Values should not be equal")  # Returns False and logs a failure message

    """
    __tracebackhide__ = True
    if first_value != second_value:
        return True
    log_failure(f"check {first_value} != {second_value}", msg)
    return False


def is_(first_value, second_value, msg=""):
    """
    Check if two values refer to the same object.

    Parameters:
    - first_value: The first value for comparison.
    - second_value: The second value for comparison.
    - msg (optional): A custom error message to include if the values are not the same object.

    Returns:
    - bool: True if `first_value` is the same object as `second_value`, False otherwise.

    Example:
    >>> is_(3, 3)  # Returns True
    >>> is_("hello", "world", "Values should be the same object")  # Returns False and logs a \
    failure message

    """
    __tracebackhide__ = True
    if first_value is second_value:
        return True
    log_failure(f"check {first_value} is {second_value}", msg)
    return False


def is_not(first_value, second_value, msg=""):
    """
    Check if two values do not refer to the same object.

    Parameters:
    - first_value: The first value for comparison.
    - second_value: The second value for comparison.
    - msg (optional): A custom error message to include if the values are the same object.

    Returns:
    - bool: True if `first_value` is not the same object as `second_value`, False otherwise.

    Example:
    >>> is_not(3, 4)  # Returns True
    >>> is_not("hello", "hello", "Values should not be the same object")  # Returns False and logs \
    a failure message

    """
    __tracebackhide__ = True
    if first_value is not second_value:
        return True
    log_failure(f"check {first_value} is not {second_value}", msg)
    return False


def is_true(value, msg=""):
    """
    Check if a given value evaluates to True.

    Parameters:
    - value: The value to check.
    - msg (optional): A custom error message to include if the check fails.

    Returns:
    - bool: True if `bool(value)` is True, False otherwise.

    Example:
    >>> is_true(1)  # Returns True
    >>> is_true(0, "Value should be True")  # Returns False and logs a failure message

    """
    __tracebackhide__ = True
    if bool(value):
        return True
    log_failure(msg)
    return False


def is_false(value, msg=""):
    """
    Check if a given value evaluates to False.

    Parameters:
    - value: The value to check.
    - msg (optional): A custom error message to include if the check fails.

    Returns:
    - bool: True if `bool(value)` is False, False otherwise.

    Example:
    >>> is_false(0)  # Returns True
    >>> is_false(1, "Value should be False")  # Returns False and logs a failure message

    """
    __tracebackhide__ = True
    if not bool(value):
        return True
    log_failure(f"check not bool({value})", msg)
    return False


def is_none(value, msg=""):
    """
    Check if a given value is None.

    Parameters:
    - value: The value to check.
    - msg (optional): A custom error message to include if the check fails.

    Returns:
    - bool: True if `value` is None, False otherwise.

    Example:
    >>> is_none(None)  # Returns True
    >>> is_none(42, "Value should be None")  # Returns False and logs a failure message

    """
    __tracebackhide__ = True
    if value is None:
        return True
    log_failure(f"check {value} is None", msg)
    return False


def is_not_none(value, msg=""):
    """
    Check if a given value is not None.

    Parameters:
    - value: The value to check.
    - msg (optional): A custom error message to include if the check fails.

    Returns:
    - bool: True if `value` is not None, False otherwise.

    Example:
    >>> is_not_none(42)  # Returns True
    >>> is_not_none(None, "Value should not be None")  # Returns False and logs a failure message

    """
    __tracebackhide__ = True
    if value is not None:
        return True
    log_failure(f"check {value} is not None", msg)
    return False


def is_in(value, iterable, msg=""):
    """
    Check if a value is present in a given iterable.

    Parameters:
    - value: The value to check for.
    - iterable: The iterable to search in.
    - msg (optional): A custom error message to include if the check fails.

    Returns:
    - bool: True if `value` is present in `iterable`, False otherwise.

    Example:
    >>> is_in(3, [1, 2, 3, 4])  # Returns True
    >>> is_in('x', 'abc', "Value should be present")  # Returns False and logs a failure message

    """
    __tracebackhide__ = True
    if value in iterable:
        return True
    log_failure(f"check {value} in {iterable}", msg)
    return False


def is_not_in(value, iterable, msg=""):
    """
    Check if a value is not present in a given iterable.

    Parameters:
    - value: The value to check for absence.
    - iterable: The iterable to search in.
    - msg (optional): A custom error message to include if the check fails.

    Returns:
    - bool: True if `value` is not present in `iterable`, False otherwise.

    Example:
    >>> is_not_in('x', 'abc')  # Returns True
    >>> is_not_in(3, [1, 2, 3, 4], "Value should not be present")  # Returns False and logs a \
    failure message

    """
    __tracebackhide__ = True
    if value not in iterable:
        return True
    log_failure(f"check {value} not in {iterable}", msg)
    return False


def is_instance(value, type_to_check, msg=""):
    """
    Check if a value is an instance of a specified type.

    Parameters:
    - value: The value to check.
    - type_to_check: The type to check against.
    - msg (optional): A custom error message to include if the check fails.

    Returns:
    - bool: True if `value` is an instance of `type_to_check`, False otherwise.

    Example:
    >>> is_instance('hello', str)  # Returns True
    >>> is_instance(42, str, "Value should be a string")  # Returns False and logs a failure message

    """
    __tracebackhide__ = True
    if isinstance(value, type_to_check):
        return True
    log_failure(f"check isinstance({value}, {type_to_check})", msg)
    return False


def is_not_instance(value, type_to_check, msg=""):
    """
    Check if a value is not an instance of a specified type.

    Parameters:
    - value: The value to check.
    - type_to_check: The type to check against.
    - msg (optional): A custom error message to include if the check fails.

    Returns:
    - bool: True if `value` is not an instance of `type_to_check`, False otherwise.

    Example:
    >>> is_not_instance(42, str)  # Returns True
    >>> is_not_instance('hello', str, "Value should not be a string")  # Returns False and logs a \
    failure message

    """
    __tracebackhide__ = True
    if not isinstance(value, type_to_check):
        return True
    log_failure(f"check not isinstance({value}, {type_to_check})", msg)
    return False


def almost_equal(first_value, second_value, rel=None, abs_tol=None, msg=""):
    """
    Check if two values are almost equal within the specified relative and absolute tolerances.

    Parameters:
    - first_value: The first value for comparison.
    - second_value: The second value for comparison.
    - rel (optional): Relative tolerance. If provided, it is used for the relative comparison.
    - abs_tol (optional): Absolute tolerance. If provided, it is used for the absolute comparison.
    - msg (optional): A custom error message to include if the check fails.

    Returns:
    - bool: True if `first_value` is almost equal to `second_value` within the specified tolerances\
        , False otherwise.

    Example:
    >>> almost_equal(1.0, 1.1, rel=0.1)  # Returns True
    >>> almost_equal(1.0, 1.2, rel=0.1, abs_tol=0.05, msg="Values should be almost equal")  # \
    Returns False and logs a failure message

    """

    __tracebackhide__ = True
    if first_value == pytest.approx(second_value, rel, abs_tol):
        return True
    log_failure(
        f"check {first_value} == pytest.approx({second_value}, rel={rel}, abs_tol={abs_tol})", msg)
    return False


def not_almost_equal(first_value, second_value, rel=None, abs_tol=None, msg=""):
    """
    Check if two values are not almost equal within the specified relative and absolute tolerances.

    Parameters:
    - first_value: The first value for comparison.
    - second_value: The second value for comparison.
    - rel (optional): Relative tolerance. If provided, it is used for the relative comparison.
    - abs_tol (optional): Absolute tolerance. If provided, it is used for the absolute comparison.
    - msg (optional): A custom error message to include if the check fails.

    Returns:
    - bool: True if `first_value` is not almost equal to `second_value` within the specified \
        tolerances, False otherwise.

    Example:
    >>> not_almost_equal(1.0, 1.1, rel=0.1)  # Returns False and logs a failure message
    >>> not_almost_equal(1.0, 1.2, rel=0.1, abs_tol=0.05, msg="Values should not be almost equal") \
          # Returns True

    """
    __tracebackhide__ = True
    if first_value != pytest.approx(second_value, rel, abs_tol):
        return True
    log_failure(
        f"check {first_value} != pytest.approx({second_value}, rel={rel}, abs_tol={abs_tol})", msg)
    return False


def greater(first_value, second_value, msg=""):
    """
    Check if the first value is greater than the second.

    Parameters:
    - first_value: The first value for comparison.
    - second_value: The second value for comparison.
    - msg (optional): A custom error message to include if the check fails.

    Returns:
    - bool: True if `first_value` is greater than `second_value`, False otherwise.

    Example:
    >>> greater(3, 2)  # Returns True
    >>> greater(2, 3, msg="Value should be greater")  # Returns False and logs a failure message

    """
    __tracebackhide__ = True
    if first_value > second_value:
        return True
    log_failure(f"check {first_value} > {second_value}", msg)
    return False


def greater_equal(first_value, second_value, msg=""):
    """
    Check if the first value is greater than or equal to the second.

    Parameters:
    - first_value: The first value for comparison.
    - second_value: The second value for comparison.
    - msg (optional): A custom error message to include if the check fails.

    Returns:
    - bool: True if `first_value` is greater than or equal to `second_value`, False otherwise.

    Example:
    >>> greater_equal(3, 2)  # Returns True
    >>> greater_equal(2, 3, msg="Value should be greater or equal")  # Returns False and logs a \
    failure message

    """
    __tracebackhide__ = True
    if first_value >= second_value:
        return True
    log_failure(f"check {first_value} >= {second_value}", msg)
    return False


def less(first_value, second_value, msg=""):
    """
    Check if the first value is less than the second.

    Parameters:
    - first_value: The first value for comparison.
    - second_value: The second value for comparison.
    - msg (optional): A custom error message to include if the check fails.

    Returns:
    - bool: True if `first_value` is less than `second_value`, False otherwise.

    Example:
    >>> less(2, 3)  # Returns True
    >>> less(3, 2, msg="Value should be less")  # Returns False and logs a failure message

    """
    __tracebackhide__ = True
    if first_value < second_value:
        return True
    log_failure(f"check {first_value} < {second_value}", msg)
    return False


def less_equal(first_value, second_value, msg=""):
    """
    Check if the first value is less than or equal to the second.

    Parameters:
    - first_value: The first value for comparison.
    - second_value: The second value for comparison.
    - msg (optional): A custom error message to include if the check fails.

    Returns:
    - bool: True if `first_value` is less than or equal to `second_value`, False otherwise.

    Example:
    >>> less_equal(2, 3)  # Returns True
    >>> less_equal(3, 2, msg="Value should be less or equal")  # Returns False and logs a failure \
    message

    """
    __tracebackhide__ = True
    if first_value <= second_value:
        return True
    log_failure(f"check {first_value} <= {second_value}", msg)
    return False


def between(value_to_check, lower_bound, upper_bound, msg="", lower_bound_included=False, \
            upper_bound_included=False):
    """
    Check if a value is between two other values.

    Parameters:
    - value_to_check: The value to check.
    - lower_bound: The lower bound.
    - upper_bound: The upper bound.
    - lower_bound_included (optional): If True, the check is inclusive on the lower bound.
    - upper_bound_included (optional): If True, the check is inclusive on the upper bound.
    - msg (optional): A custom error message to include if the check fails.

    Returns:
    - bool: True if `value_to_check` is between `lower_bound` and `upper_bound` (inclusive or \
        exclusive based on `lower_bound_included` and `upper_bound_included`), False otherwise.

    Example:
    >>> between(3, 2, 4)  # Returns True
    >>> between(2, 2, 4, lower_bound_included=True, upper_bound_included=True)  # Returns True
    >>> between(5, 2, 4)  # Returns False and logs a failure message

    """
    __tracebackhide__ = True
    if lower_bound_included and upper_bound_included:
        if lower_bound <= value_to_check <= upper_bound:
            return True
        log_failure(
            f"check {lower_bound} <= {value_to_check} <= {upper_bound}", msg)
        return False
    if lower_bound_included:
        if lower_bound <= value_to_check < upper_bound:
            return True
        log_failure(
            f"check {lower_bound} <= {value_to_check} < {upper_bound}", msg)
        return False
    if upper_bound_included:
        if lower_bound < value_to_check <= upper_bound:
            return True
        log_failure(
            f"check {lower_bound} < {value_to_check} <= {upper_bound}", msg)
        return False
    if lower_bound < value_to_check < upper_bound:
        return True
    log_failure(
        f"check {lower_bound} < {value_to_check} < {upper_bound}", msg)
    return False
