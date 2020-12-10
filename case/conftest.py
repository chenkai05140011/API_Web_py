import requests
import pytest
from case.IssueCheck.common_issuecheck import Test_LiaisonMan
from case.common_function import LogIn

#case公共前置条件



@pytest.fixture(scope="module")
def login_fix():
    s = requests.session()
    re = LogIn(s)
    re.login()
    return s


#case公共前置条件
@pytest.fixture(scope="module")
def login_fix1():
    s = requests.session()
    re = Login(s)
    re.login()
    return s

#case公共前置后置条件
@pytest.fixture(scope='function')
def delete_all_liaisonman(login_fix):
    re = Test_LiaisonMan(login_fix)
    res = re.delete_all_liaisonman()
    yield
    re = Test_LiaisonMan(login_fix)
    res = re.delete_all_liaisonman()