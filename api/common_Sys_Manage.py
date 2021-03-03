import requests
import json
import allure
#case公共类和函数

class Sys_Manage(object):

    def __init__(self, s, host="http://59.202.63.108:80"):
        self.host = host
        self.s = s
    # 获取领域列表
    @allure.step("获取领域列表")
    def get_territory_list(self, permissionFilter=True, orgFilter=True, deptType=2, hasSelf=True):
        url = self.host + "/api/v2/sysmanage/territory/getTerritoryList"
        data = {'permissionFilter': permissionFilter,
                "orgFilter": orgFilter,
                "deptType": deptType,
                "hasSelf": hasSelf}
        r = self.s.get(url=url, params=data)
        return r.json()

    # 获取领域机构树
    @allure.step("获取领域机构树")
    def get_territory_org_dept_tree(self, territoryId=137, permissionFilter=True, orgFilter=True, deptType=2, hasSelf=True):
        url = self.host + "/api/v2/sysmanage/territory/getTerrioryOrgDeptTree"
        data = {'territoryId': territoryId,
                "permissionFilter": permissionFilter,
                "orgFilter": orgFilter,
                "deptType": deptType,
                "hasSelf": hasSelf
                }
        r = self.s.get(url=url, params=data)
        return r.json()