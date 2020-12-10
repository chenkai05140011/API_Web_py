import time

import pytest
import requests
import json
import allure
from case.common_orgEntity import Org_Entity
from case.common_Sys_Manage import Sys_Manage

#pytest --alluredir ./report/allure_raw 导出报告
#allure serve report/allure_raw 运行allue服务


# @pytest.fixture(scope="function")
# def tag_fix():
#     print("前置数据准备")
#     yield "删除完成"
#     print("后置数据清理")

# 前置后置处理
# _module模块级别
# _class类级别
# _function函数级别
#_method方法级别
# def setup_class():
#     pass
# def teardown_class():
#     pass


# @allure.feature("dome")#一个完整功能点（模块）
# class TestCC():
#     @allure.story("测试用例2")  # 一个完整测试用例
#     def test_4(self):
#         print("测试用例2")
#
#         @allure.step("步骤1")  # 一个完整测试用例
#         def test_3(self):
#             print("步骤1")


# @pytest.mark.skip("阻塞BUG")
#标注可以按照标记去执行测试用例pytest -v -m webtest

#pytest参数化
@pytest.mark.api_select
@allure.story("机构类查询场景参数化")#一个完整测试用例
@pytest.mark.parametrize("test_input,expect", [("日用口罩", 200), ("清洁球", 200), (1, 200)])
def test_sel_jgl(login_fix, test_input, expect):
    '''
        用例描述：监管对象（机构类）查询接
        :param login_fix:前置登入
        :return:
        '''
    s = login_fix
    re = Org_Entity(s)
    # step1 执行查询
    data = re.select_org_entity(test_input)
    assert data["code"] == expect


#pytest笛卡尔积(参数化)
@pytest.mark.api_select
@allure.story("测试机构类查询场景笛卡尔积(参数化)")#一个完整测试用例
@pytest.mark.parametrize("test_input_1", ["日用口罩", "清洁球"])
@pytest.mark.parametrize("test_input_2", [0, 1, 2, 4, 5, 6, 9])
def test_sel1_jgl(login_fix, test_input_1, test_input_2):
    '''
        用例描述：监管对象（机构类）查询接（名称和主体类型）
        :param login_fix:前置登入
        :return:
    '''
    s = login_fix
    re = Org_Entity(s)
    # step1 执行查询
    data = re.select_org_entity(test_input_1,test_input_2)
    assert data["code"] == 200

@pytest.mark.api_test
@allure.story("移除机构管辖")#一个完整测试用例
def test_del_jgl(login_fix):
    '''
    用例描述：监管对象（机构类）移除操作依赖查询返回uid
    :param login_fix:前置登入
    :return:
    '''
    s = login_fix
    re = Org_Entity(s)
    # step1 执行查询
    data = re.select_org_entity()
    assert data["code"] == 200
    # 组合依赖数据
    uid_1 = data["data"]["data"][0]["uid"]
    uid_2 = data["data"]["data"][1]["uid"]
    uid = []
    uid.append(uid_1)
    uid.append(uid_2)
    # step2 执行移除接口
    data_1 = re.del_org_entity(uid)
    assert data_1['message'] == "批量移除管辖成功"

@pytest.mark.api_test
@allure.story("添加机构类管辖")#一个完整测试用例
def test_add_jgl(login_fix):
    '''
    用例描述：监管对象（机构类）添加机构类管辖
    :param login_fix:前置登入
    :return:
    '''
    s = login_fix
    re = Org_Entity(s)
    # step1 执行查询
    data = re.select_zh_org_entity(1)#1可认领
    assert data["code"] == 200
    # 组合依赖数据
    pripid_1 = data["data"]["data"][0]["pripid"]
    pripid_2 = data["data"]["data"][1]["pripid"]
    pripid = []
    pripid.append(pripid_1)
    pripid.append(pripid_2)
    # step2 执行移除接口
    data_1 = re.add_org_entity(pripid)
    assert data_1['message'] == "批量加入管辖成功:2条,失败：0条"

@pytest.mark.api_test
@allure.story("指派机构类管辖")#一个完整测试用例
def test_add_jgl(login_fix):
    '''
    用例描述：监管对象（机构类）添加机构类管辖
    :param login_fix:前置登入
    :return:
    '''
    s = login_fix
    re = Org_Entity(s)
    # step1 执行查询
    data = re.select_zh_org_entity(1)#1可认领
    assert data["code"] == 200
    # 组合依赖数据
    pripid_1 = data["data"]["data"][0]["pripid"]
    pripid_2 = data["data"]["data"][1]["pripid"]
    pripid = []
    pripid.append(pripid_1)
    pripid.append(pripid_2)
    # step2 执行移除接口
    data_1 = re.add_org_entity(pripid)
    assert data_1['message'] == "批量加入管辖成功:2条,失败：0条"

@pytest.mark.api_test
@allure.story("添加主体-查询主体-移除主体")
def test_cs001_jgl(login_fix):
    '''
    用例描述：添加主体-查询主体-—移除主体
    :param login_fix:前置登入
    :return:
    '''
    s = login_fix
    re = Org_Entity(s)
    # step1 执行查询
    data = re.select_zh_org_entity(orgEntityName="跃驰", avaliable=1)#1可认领
    assert data["code"] == 200
    print(data)
    # 组合依赖数据
    pripid_1 = data["data"]["data"][0]["pripid"]
    pripid = []
    pripid.append(pripid_1)
    # step2 执行移除接口
    data_1 = re.add_org_entity(pripid)
    print(data_1)
    assert data_1['message'] == "批量加入管辖成功"
    orgEntityName = data["data"]["data"][0]["orgEntityName"]
    print(orgEntityName)
    time.sleep(20)
    data_2 = re.select_org_entity(orgEntityName=orgEntityName, regState=1)
    print(data_2)
    assert data_2['data']['data'][0]['pripid'] in pripid
    # step指派
    uid = data_2['data']['data'][0]['uid']
    uid_list = []
    uid_list.append(uid)
    manageCode = data_2['data']['data'][0]['manageCode']
    manageType = data_2['data']['data'][0]['manageType']
    data_assign = re.assign_org_entity(uid=uid_list,  manageCode=manageCode, manageType=manageType)
    assert data_assign == "批量指派成功:1条,失败:0条"
    # 移除
    data_del = re.del_org_entity(uid=uid_list)
    assert data_del == "批量移除成功:1条,失败:0条"
    return data_2['data']['data'][0]['pripid']















