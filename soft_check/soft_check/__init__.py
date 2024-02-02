import pytest

pytest.register_assert_rewrite("soft_check.check_functions")

from soft_check.context_manager import check
from soft_check.check_raises import raises
from soft_check.check_log import any_failures
from soft_check.check_functions import *
from soft_check import check_functions


setattr(check, "raises", raises)
setattr(check, "any_failures", any_failures)
setattr(check, "check", check)

for func in check_functions.__all__:
    setattr(check, func, getattr(check_functions, func))
