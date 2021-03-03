import requests
import pytest

from api.common_function import LogIn

#case公共前置条件



@pytest.fixture(scope="module")
def login_fix():
    s = requests.session()
    re = LogIn(s)
    re.login()
    return s