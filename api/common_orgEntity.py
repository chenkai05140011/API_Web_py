import requests
import json
import allure
#case公共类和函数



# 监管对象机构类

class Org_Entity(object):

    def __init__(self, s, host="http://59.202.63.108:80"):
        self.host = host
        self.s = s
    # 查询机构主体
    @allure.step("机构主体_查询管辖")
    def select_org_entity(self, orgEntityName=None, regState=None):
        url = self.host + "/api/v2/supervision/orgEntity/selectOrgEntityList"
        data = {
        "length":10,
        "pageNum":1,
        "orgEntityCategory":"",
        "orgEntityName":orgEntityName,
        "unicodeRegno":"",
        "regState":regState,
        "manageCode":"",
        "gridAreaCode":"",
        "managePersonName":"",
        "cityCode":"",
        "areaCode":"",
        "townCode":"",
        "tagCode":"",
        "manageUserMarked":"",
        "addressCompare":"",
        "markAddress":"",
        "leRep":"",
        "leRepCertNo":"",
        "estDateStart":"",
        "estDateEnd":"",
        "apprDateStart":"",
        "apprDateEnd":"",
        "regDeptCode":"",
        "opScope":"",
        "regAddress":"",
        "dataAttribute":"",
        "updateTimeStart":"",
        "updateTimeEnd":""
        }
        r = self.s.post(url=url, json=data)
        return r.json()

    # 查询中合库机构主体
    @allure.step("机构主体_查询中合库")
    def select_zh_org_entity(self,orgEntityName=None, avaliable=None):
        url = self.host + "/api/v2/supervision/orgEntity/selectEnableManageOrgEntityList"
        data = {
        "length":10,
        "pageNum":1,
        "orgEntityCategory":"",
        "orgEntityName":orgEntityName,
        "unicodeRegno":"",
        "regState":"1",
        "cityCode":"",
        "areaCode":"",
        "townCode":"",
        "avaliable":avaliable,
        "isExclue":"true"
        }
        r = self.s.post(url=url, json=data)
        return r.json()

    # 机构主体加入管辖
    @allure.step("机构主体_加入管辖")
    def add_org_entity(self, pripid=None):
        url = self.host + "/api/v2/supervision/orgEntity/batchAddOrgEntityManage"
        data = {"data": pripid
                }
        r = self.s.post(url=url, json=data)
        return r.json()

    # 移除
    @allure.step("机构主体_移除")
    def del_org_entity(self, uid):
        url = self.host + "/api/v2/supervision/orgEntity/batchOrgEntityManageDel"
        data = {"data": uid}
        r = self.s.post(url=url, json=data)
        return r.json()

    # 机构——指派管辖
    @allure.step("机构主体_指派管辖")
    def assign_org_entity(self, uid, manageCode, manageType):
        url = self.host + "/api/v2/supervision/orgEntity/orgEntityManageadd"
        data = {"uidList": uid,
                "manageCode": manageCode,
                "manageType": manageType,
                "addManageType": "2",
                "addManageCode": "3307820002301016"
                }
        r = self.s.post(url=url, json=data)
        return r.json()

    # 标注
    @allure.step("机构主体_标注")
    def del_org_entity(self, uid):
        url = self.host + "/api/v2/supervision/orgEntity/batchOrgEntityManageDel"
        data = {"data": uid}
        r = self.s.post(url=url, json=data)
        return r.json()







# if __name__ == '__main__':
#     re = OrgEntityList()
#     print(re.select_jgzt())
