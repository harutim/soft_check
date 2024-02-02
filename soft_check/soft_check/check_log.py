"""
check_log.py

This module provides functions to manage and log test failures.

Functions:
- clear_failures: Clear the stored failures and reset the maximum failure count and reporting \
    limits.
- any_failures: Check if there are any stored failures.
- get_failures: Get the list of stored failures.
- log_failure: Log a failure message.

Example usage:
--------------
# Import the module
from soft_check import check_log

# Clear failures at the beginning of a test run
check_log.clear_failures()

# Perform tests and log failures as needed
if some_condition:
    log_failure("Test case 1 failed due to some_condition.", "Additional information about the \
        check.")

# Check if there are any recorded failures
if any_failures():
    print("Test run completed with failures. Details:")
    # Get and print the list of failures
    failures = get_failures()
    for failure in failures:
        print(failure)
else:
    print("Test run completed successfully.")

"""
SHOULD_USE_COLOR = False
COLOR_RED = "\x1b[31m"
COLOR_RESET = "\x1b[0m"
_STOP_ON_FAIL = False

_DEFAULT_MAX_FAIL = None
_DEFAULT_MAX_REPORT = None
_DEFAULT_MAX_TB = None

_MAX_FAIL = None
_MAX_REPORT = None
_MAX_TB = None
_NUM_FAILURES = 0

_failures = []

def clear_failures():
    """
    Clear the stored failures and reset the maximum failure count and reporting limits.
    """
    global _failures, _NUM_FAILURES
    global _MAX_FAIL, _MAX_REPORT, _MAX_TB
    _failures = []
    _NUM_FAILURES = 0
    _MAX_FAIL = _DEFAULT_MAX_FAIL
    _MAX_REPORT = _DEFAULT_MAX_REPORT
    _MAX_TB = _DEFAULT_MAX_TB


def any_failures() -> bool:
    """
    Check if there are any stored failures.

    Returns:
    - bool: True if there are failures, False otherwise.
    """
    return bool(get_failures())


def get_failures():
    """
    Get the list of stored failures.

    Returns:
    - list: A list of failure messages.
    """
    return _failures


def log_failure(msg="", check_str=""):
    """
    Log a failure message.

    Args:
    - msg (str): The main failure message.
    - check_str (str): Additional information about the check.

    Global Variables:
    - _NUM_FAILURES (int): Counter for the number of failures.
    - _MAX_REPORT (int): Maximum number of failures to report.
    - _MAX_FAIL (int): Maximum number of failures before raising an assertion.
    - _failures (list): List to store failure messages.
    - _STOP_ON_FAIL (bool): Whether to stop on the first failure.

    Returns:
    - None
    """
    global _NUM_FAILURES
    __tracebackhide__ = True
    _NUM_FAILURES += 1

    msg = str(msg).strip()

    if check_str:
        msg = f"{msg}: {check_str}"

    if (_MAX_REPORT is None) or (_NUM_FAILURES <= _MAX_REPORT):

        if SHOULD_USE_COLOR:
            msg = f"{COLOR_RED}{msg}{COLOR_RESET}"
        _failures.append(msg)

    if _MAX_FAIL and (_NUM_FAILURES >= _MAX_FAIL):
        assert_msg = f"pytest-check max fail of {_NUM_FAILURES} reached"
        assert _NUM_FAILURES < _MAX_FAIL, assert_msg

    if _STOP_ON_FAIL:
        assert False, "Stopping on first failure"
