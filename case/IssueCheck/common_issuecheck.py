import json

import allure
from CONFIG.Define import LogLevel
from COMMON import Log
from CONFIG.Global import JGPC


class Test_LiaisonMan():

    def __init__(self,s,host=JGPC):
        self.s = s
        self.host = host

    @allure.step("新增联络员")
    def addliaisonman(self,businessType=None,remindType=None,liaName='杨一帆1'):
        Log.LogOutput(level=LogLevel.INFO, message='开始新增联络员')
        url = self.host + "/api/v2/clueCenter/clueMechanismLiaison/saveLiaisonMan"
        data = {
            "clueMechanismLiaisonDTOS":[{"deptNode":"3307820001301157",
                                             "businessType":businessType,  #业务类型：1审核业务，2处置业务.
                                             "clueType":"1",
                                             "remindType":remindType,      #消息媒介：1站内 2钉消息 3短信
                                             "sourceSystemid":"1",
                                             "liaisonInfoList":[{"deptName":"办公室",
                                                                 "deptNode":"3307820001301157",
                                                                 "mechanismName":"义乌市市场监督管理局",
                                                                 "mechanismCode":"330782000000_11330782097919258G",
                                                                 "phone":"13588012414",
                                                                 "liaName":liaName,
                                                                 "userid":"40263"}]}]
        }
        r = self.s.post(url=url,json=data)
        if r.json()['code'] == 200:
            Log.LogOutput(level=LogLevel.INFO, message='联络员新增成功')
        else:
            Log.LogOutput(level=LogLevel.ERROR, message='新增失败，请检查参数信息')
        return r.json()

    @allure.step("编辑联络员")
    def editliaisonman(self,remindType= None):
        Log.LogOutput(level=LogLevel.INFO, message='开始编辑联络员')
        url = self.host + '/api/v2/clueCenter/clueMechanismLiaison/editDeptLiaison'
        data = {
            "businessType":"1",
                "clueType":"1",
                "remindType":remindType,
                "sourceSystemid":"1",
                "liaisonInfoList":[{"deptName":"办公室",
                                    "deptNode":"3307820001301157",
                                    "mechanismName":"义乌市市场监督管理局",
                                    "mechanismCode":"330782000000_11330782097919258G",
                                    "phone":"13588012414",
                                    "liaName":"杨一帆1",
                                    "userid":"40263"}],
                "clueliaid":"3ae30164140849e194609c6022c734a4"
                }
        r = self.s.post(url=url,json=data)
        if r.json()['message'] == '编辑成功':
            Log.LogOutput(level=LogLevel.INFO,message='编辑联络员成功')
        else:
            Log.LogOutput(level=LogLevel.ERROR, message='编辑失败，请检查参数信息')
        return r.json()

    @allure.step("查询联络员")
    def selectliaisonman(self,businessType=None,liaName='杨一帆1',mechanismCode='330782000000_11330782097919258G',phone='13588012414'):
        Log.LogOutput(level=LogLevel.INFO, message='开始查询联络员列表')
        url = self.host + '/api/v2/clueCenter/clueMechanismLiaison/queryLiaisonList'
        data = {"length": 10,
                "pageNum": 1,
                "clueType": "1",
                "businessType": businessType,
                "mechanismCode": mechanismCode,
                "liaName": liaName,
                "phone": phone
                }
        r = self.s.post(url=url, json=data)
        if r.json()['message'] == '查询成功':
            Log.LogOutput(level=LogLevel.INFO, message='查询联络员成功')
        else:
            Log.LogOutput(level=LogLevel.ERROR, message='查询失败，请检查参数信息')
        return r.json()


    @allure.step("删除联络员")
    def deleteliaisonman(self,clueliaid=None):
        Log.LogOutput(level=LogLevel.INFO, message='开始删除联络员')
        url = self.host + '/api/v2/clueCenter/clueMechanismLiaison/delDeptLiaison'
        data = {
            'clueliaid':clueliaid
        }
        r = self.s.get(url=url,params=data)
        if r.json()['message'] == '删除成功':
            Log.LogOutput(level=LogLevel.INFO,message='删除联络员成功')
        else:
            Log.LogOutput(level=LogLevel.ERROR, message='删除失败，请检查参数信息')
        return r.json()
    @allure.step("删除所有联络员")
    def delete_all_liaisonman(self):
        Log.LogOutput(level=LogLevel.INFO, message='开始删除联络员列表所有数据')
        # 获取列表
        res = self.selectliaisonman()
        if res['message'] != '查询成功':
            Log.LogOutput(level=LogLevel.DEBUG, message='列表查询失败')
            return False
        ids = ''
        for item in res['data']['data']:
            ids = ids + str(item['clueliaid']) + ','
        Log.LogOutput(level=LogLevel.INFO, message=ids)
        # 去除最后的“,”
        ids = ids[:-1]
        Log.LogOutput(level=LogLevel.INFO, message=ids)
        delComprehensiveMemDict = ids
        response = self.deleteliaisonman(clueliaid=delComprehensiveMemDict)
        if response['message'] == '删除成功':
            Log.LogOutput(level=LogLevel.INFO, message='数据删除成功')
            return True
        # elif response[1:5] in "请选择要删除的记录!":
        #     Log.LogOutput(level=LogLevel.INFO, message='数据删除成功')
        #     return True
        else:
            Log.LogOutput(level=LogLevel.ERROR, message='数据删除失败')
            return False