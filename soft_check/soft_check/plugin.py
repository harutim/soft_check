import sys
import warnings

import pytest
from _pytest._code.code import ExceptionInfo
from _pytest.skipping import xfailed_key

from soft_check import check_log, check_raises, context_manager, pseudo_traceback


@pytest.hookimpl(trylast=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    A pytest hook to customize the test report.

    Args:
    - item: Test item.
    - call: Test call.

    Returns:
    - None
    """
    outcome = yield
    report = outcome.get_result()

    failures = check_log.get_failures()
    check_log.clear_failures()

    if failures:
        longrepr = ["\n".join(failures)]
        report.longrepr = "\n".join(longrepr)

        if item._store[xfailed_key]:
            report.outcome = "skipped"
            report.wasxfail = item._store[xfailed_key].reason
        else:
            report.outcome = "failed"

        try:
            raise AssertionError(report.longrepr)
        except AssertionError:
            excinfo = ExceptionInfo.from_current()
        call.excinfo = excinfo

def pytest_configure(config):
    """
    A pytest hook to configure and set up check-related options.

    Args:
    - config: Pytest configuration object.

    Returns:
    - None
    """
    # Add some red to the failure output, if stdout can accommodate it.
    isatty = sys.stdout.isatty()
    color = config.option.color
    check_log.should_use_color = (isatty and color == "auto") or (color == "yes")

    # If -x or --maxfail=1, then stop on the first failed check
    # Otherwise, let pytest stop on the maxfail-th test function failure
    maxfail = config.getvalue("maxfail")
    stop_on_fail = maxfail == 1

    context_manager._stop_on_fail = stop_on_fail
    check_raises._stop_on_fail = stop_on_fail
    check_log._stop_on_fail = stop_on_fail

    # Allow for --tb=no to turn off check's pseudo tbs
    traceback_style = config.getvalue("tbstyle")
    pseudo_traceback._traceback_style = traceback_style

    # Grab options
    check_log._default_max_fail = config.getoption("--check-max-fail")
    check_log._default_max_report = config.getoption("--check-max-report")
    check_log._default_max_tb = config.getoption("--check-max-tb")
    no_tb = config.getoption("--check-no-tb")
    if no_tb:
        warnings.warn(
            "--check-no-tb is deprecated; use --check-max-tb=0", DeprecationWarning
        )
        check_log._default_max_tb = 0

@pytest.fixture(name="check")
def check_fixture():
    """
    Pytest fixture to provide the `check` instance.

    Returns:
    - CheckContextManager: An instance of the `CheckContextManager`.
    """
    return context_manager.check

def pytest_addoption(parser):
    """
    Pytest hook to add custom command line options for pytest-check.

    Args:
    - parser: The pytest parser object.

    Options:
    - "--check-no-tb": Turn off pseudo-tracebacks.
    - "--check-max-report": Set the maximum failures to report.
    - "--check-max-fail": Set the maximum failures per test.
    - "--check-max-tb": Set the maximum pseudo-tracebacks per test.
    """
    parser.addoption(
        "--check-no-tb",
        action="store_true",
        help="turn off pseudo-tracebacks",
    )
    parser.addoption(
        "--check-max-report",
        action="store",
        type=int,
        help="max failures to report",
    )
    parser.addoption(
        "--check-max-fail",
        action="store",
        type=int,
        help="max failures per test",
    )
    parser.addoption(
        "--check-max-tb",
        action="store",
        type=int,
        default=1,
        help="max pseudo-tracebacks per test",
    )
