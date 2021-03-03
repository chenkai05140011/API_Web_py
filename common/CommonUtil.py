#!/usr/bin/env python
# -*- coding=utf-8 -*-
from __future__ import unicode_literals
import pymysql
import xlrd
from aip import AipOcr
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64
import re
import random
import json
from CONFIG import Global
from CONFIG.Define import LogLevel
import datetime
from COMMON import Log
from CONFIG.Global import responseClass
from selenium import webdriver
import time
from PIL import Image

'''
    @功能：     在某一字符串中匹配特定的字符串
    @para: 
    stringOrg: 原字符串
    stringReg: 待匹配的字符串
    @return: 如果匹配成功，则返回True；否则返回False   
'''

def regMatchString(stringOrg,stringReg):
    expected_regexp = re.compile(str(stringReg))
    match = expected_regexp.search(str(stringOrg))
    if match:
 #       print('字符串匹配成功')
        return True
    else:
 #       print('字符串匹配失败')
        return False

'''
    @功能：     比较两个字典Dict1和Dict的键值
    @para: 
    Dict1: 待比较的字典 或者字典列表
    Dict: 待查找的字典
    @return: 如果DictList中的任何一个list包含Dict中所有不为None的键，且键值相同，则返回True；否则返回False   
'''
def findDictInDictlist(Dict,DictList):
    compareResult = False
    for dictItem in DictList:
        itemExist = 0
        for (d,x) in Dict.items():
            if x is None:
                continue
            keyValue = (d,x)
            if dictItem.items().count(keyValue) > 0:
                continue
            else:
                itemExist = -1
                break
        if itemExist == 0:
            compareResult = True
            break
        else:
            continue
    return compareResult

'''
    @功能：     对http报文的response进行解析，并返回一个类，包含解析后的结果、状态、及text属性
    @para: 
    httpResponse: http报文响应
    @return: 如果一个类的对象，类中有result、statusLine及text三个属性 
'''
def httpResponseResultDeal(httpResponse):
    responseObject = responseClass()
    responseObject.result = False
    if httpResponse is not None:
        responseObject.text = httpResponse.text
        responseObject.statusLine = httpResponse.status_code
        responseObject.content = httpResponse.content
        try:
            #当返回不为json时，该函数会抛出异常
            responseDict = json.loads(httpResponse.text)
            if responseDict.has_key('message'):
                if responseDict['message']!="成功":
                    responseObject.result = False
                    return responseObject
            if responseDict.has_key('mobileSign'):
                if responseDict['mobileSign'] != "mobileSign":
                    responseObject.result = False
                    return responseObject
            if responseDict.has_key('success'):
                if responseDict['success']=="false":
                    responseObject.result = False
                    return responseObject
            responseObject.result = True
        except:          #非json可能会存在其他返回情况
            if httpResponse.status_code==200: #新增返回200表示成功
               # print('获取成功')
                responseObject.result = True
            elif httpResponse.status_code==201: #新增返回201表示成功
              #  print('服务器新增资源成功')
                responseObject.result = True
            elif httpResponse.status_code == 1:  # 新增返回1表示删除成功

                responseObject.result = True
            elif httpResponse.status_code==409: #新增时用户名已存在
            #    print('服务器已存在该记录')
                Log.LogOutput(level=LogLevel.ERROR, message='新增时该资源已存在！')
                responseObject.result = False
            elif httpResponse.status_code == 417:  # mobilelogout
            #    print('mobileLogOut!')
                responseObject.result = False
#             elif isinstance(httpResponse.text, list) and len(httpResponse.text):
            else:
                responseObject.result = False
    return responseObject

'''
  @功能 比较两个字典Dict1和Dict的键值是否相同
  @para: 方法一
  Dict1: 待比较的字典 或者字典列表
  Dict: 待查找的字典
  @return: 如果两个键值不相同的话，返回false，否则返回true
'''
def compareDictInDictlist01(Dict,Dict1):
    compareResult = False
    for dictitem in Dict:
        if dictitem=='rows':
            dict01=dictitem[0]
            for k,v in dict01.items():
                if k=='id':
                    if Dict1['id']==v:
                        compareResult = True
                        return compareResult
                        break
                else:
                    compareResult = False
                    return compareResult
    return compareResult
'''
方法二
'''
def compareDictInDictlist02(Dict,Dict1):
    compareResult = False
    if Dict.has_key('rows'): # 判断字典中是否有rows这个键
        dictitem = Dict['rows'] # 如果有，将值给dictitem，内容为一个列表 循环列表
        for dictitem01 in dictitem:#循环获取列表中的值
            dict01=dictitem01      #将列表中的字典传给dict01
            if dict01.has_key('id'):#判断是否存在id这个键
                if Dict1['id']==dict01['id']:#如果有,判断id值是否与想象值是否相同
                    compareResult = True #如果是，返回true
                    return compareResult
    else:
         compareResult = False
         return compareResult
    return compareResult


'''
获取部分字符
转换成字符串
'''
def getchar(startNum,endNum,list):
    #截取列表中的部分
    char=list[startNum:endNum]
    #将列表中的内容转换成字符串
    str=''.join(char)
    return str

'''
    @功能：     生成一个随机数字
    @para: key,length
    length:
    @return: 返回一个指定位数数字
'''

def createRandomNumber(length):
    code_list = []
    for i in range(10): # 0-9数字
         code_list.append(str(i))

    myslice = random.sample(code_list, length)  # 从list中随机获取6个元素，作为一个片断返回
    random_number = ''.join(myslice) # list to number
    return random_number


'''
    @功能：     生成一个随机数字
    @para: key,length
    length:
    @return: 返回一个指定位数数字
'''


def createRandomString2(key, length):
    code_list = []
    if key == 'number': #纯数字
        for i in range(10):  # 0-9数字
            code_list.append(str(i))
    if key == 'string': #混搭字符串
        for i in range(10):  # 0-9数字
            code_list.append(str(i))
        for i in range(65, 91):  # A-Z
            code_list.append(chr(i))
        for i in range(97, 123):  # a-z
            code_list.append(chr(i))
    if key == 'letter':#纯字符
        for i in range(65, 91):  # A-Z
            code_list.append(chr(i))
        for i in range(97, 123):  # a-z
            code_list.append(chr(i))

    myslice = random.sample(code_list, length)  # 从list中随机获取6个元素，作为一个片断返回
    random_number = ''.join(myslice)  # list to number
    return random_number


'''
    @功能： 生成一个随机字符串
    @para: 
    length: 长度
    @return: 返回一个包含大写字母和数字的字符
'''

def createRandomString(length):
    code_list = []
    for i in range(10): # 0-9数字
        code_list.append(str(i))
    for i in range(65, 91): # A-Z
        code_list.append(chr(i))
    for i in range(97, 123):  # a-z
        code_list.append(chr(i))
    myslice = random.sample(code_list, length)  # 从list中随机获取N个元素，作为一个片断返回
    random_string = ''.join(myslice) # list to string
    return random_string

'''
    @功能：     生成一个随机字母
    @para: 
    length:
    @return: 返回一个指定位数字母
'''

def createRandomLetter(length):
    code_list = []
    for i in range(65, 91):  # A-Z
        code_list.append(chr(i))
    for i in range(97, 123):  # a-z
        code_list.append(chr(i))

    myslice = random.sample(code_list, length)  # 从list中随机获取N个元素，作为一个片断返回
    random_Letter = ''.join(myslice) # list to Letter
    return random_Letter

#struts.token值
strutstoken = '%s-%s-%s-%s-%s'%(createRandomString(8),createRandomString(4),createRandomString(4),createRandomString(4),createRandomString(12))

#地区编号文件
# DC_PATH = '%s%s' % (Global.Path,'/Test_Web/Attachments/districtcode.txt')
DC_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..\\Attachments\\districtcode.txt"))


# 随机生成身份证号
def getdistrictcode():
    with open(DC_PATH, encoding='UTF-8') as file:
        data = file.read()
        districtlist = data.split('\n')
    for node in districtlist:
        if node[10:11] == ' 'and node[12:13]==' ':
            code = node[0:6]
            codelist.append({"code": code})

def gennerator():
    global codelist
    codelist = []
    if not codelist:
         getdistrictcode()
    id = codelist[random.randint(0,len(codelist))]['code'] #地区项
    id = id + str(random.randint(1930,2013)) #年份项
    da = datetime.datetime.now()+datetime.timedelta(days=random.randint(1,366)) #月份和日期项
    id = id + da.strftime('%m%d')
    id = id+ str(random.randint(100,300))#，顺序号简单处理

    i = 0
    count = 0
    weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]  # 权重项
    checkcode = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']  # 校验码
    for i in range(0, len(id)):
        count = count + int(id[i]) * weight[i]

    id = id + checkcode[(count % 11)]
    return id

#获取身份证上的生日，并用“-”分割
#id为身份证号
def birthday(id):

    date = "%s-%s-%s" % (id[6:10], id[10:12], id[12:14])

    return date

#获取性别
#id为身份证号
def gender(id):
    Sex = "%s" % (id[16:17])
    list1 = ['1','3','5','7','9']
    list2 = ['2','4','6','8','0']
    if Sex in list1:
        # 男性
        return '1'
    elif Sex in list2:
        # 女性
        return '2'
    else:
        return False



#将列表中所有的值全部转化成字符串（注：进行批量删除可以使用）
#list1为json解析后的列表，field为rows下的字段名称
def translate(list1,field):
    if list1['records'] == 0:
        Log.LogOutput(level=LogLevel.INFO, message='无记录')
    else:
        list = []
        for dictListItem in list1['rows']:
            a = dictListItem[field]
            list.append(a)
        X=','.join('%s' %id for id in list)

        return X
'''
获取列表结果判断
'''
def listCompare(dict):
    list = ['page', 'records', 'rows', 'total']
    ok = 0
    for i in list:
        if i in dict:
            ok = 1
        else:
            ok = 0
            break
    if ok == 1:
        return True
    else:
        return False

'''
list 列表
key 相应的键名
value 对比的值
num 决定返回一条数据（传参num=1）还是多条（传参num=0）数据
'''
def findData(self, list, key, value, num, output):
    itemList = []
    for item in list:
        if str(value) == str(item[key]):
            itemList.append(item)
        else:
            continue
    if num == 1:
        self.assertTrue(len(itemList) == 1, output)
        return itemList
    else:
        self.assertTrue(len(itemList) == len(list), output)
        return True


'''
查询删除的数据，查到返回false
list 列表
key 相应的键名
value 对比的值
num 决定返回一条数据（传参num=1）还是多条（传参num=0）数据
'''
def testdelete(self,list,key,value,output):
    itemList=[]

    for item in list:
        if str(value)==str(item[key]):
            itemList.append(item)
        else:
            continue

    self.assertTrue(len(itemList) == 0, output)
    return True

#str1目标字符串，str2查找字符串，截取的长度,offset偏移量是指查找字符串第一位到所取的字符串前一位的长度
def SearchStr(str1,str2,len,offset):
     a = str1.find(str2)
     str3 = str1[a+offset:a+len+offset]
     return str3

# 随机生成出生年月日
def creat_birthday():
    start_birthday = (1970,10,10,1,10,10,10,10,10)    #设置开始时间元组
    end_birthday = (2000,5,5,10,10,10,10,10,10)      #设置结束时间元组
    start = time.mktime(start_birthday)        #生成开始时间戳
    end = time.mktime(end_birthday)            #生成结束时间戳
    for i in range(1):
        s = random.randint(start,end)          #选择一个开始时间和结束时间
        date_touole = time.localtime(s)        #将时间生成元组
        date = time.strftime("%Y-%m-%d",date_touole)  #时间元组转换成格式化字符串
        return date


#男女性别随机取一个
def sex():
    List = ['96', '97']
    A = random.randrange(0, 2)
    return List[A]

'''
生成随机手机号
'''
def phoneNORandomGenerator():
    prelist=["130","131","132","133","134","135","136","137","138","139","147","150","151","152","153","155","156","157","158","159","186","187","188"]
    phone=random.choice(prelist)+"".join(random.choice("0123456789") for i in range(8))
    return phone


"""
RSA加密
Key长度2048
"""
def handle_pub_key(key):
    """
    处理公钥
    公钥格式pem，处理成以-----BEGIN PUBLIC KEY-----开头，-----END PUBLIC KEY-----结尾的格式
    :param key:pem格式的公钥，无-----BEGIN PUBLIC KEY-----开头，-----END PUBLIC KEY-----结尾
    :return:
    """
    start = '-----BEGIN PUBLIC KEY-----\n'
    end = '-----END PUBLIC KEY-----'
    result = ''
    # 分割key，每64位长度换一行
    divide = int(len(key) / 64)
    divide = divide if (divide > 0) else divide+1
    line = divide if (len(key) % 64 == 0) else divide+1
    for i in range(line):
        result += key[i*64:(i+1)*64] + '\n'
    result = start + result + end
    return result

def encrypt(key, content):
    """
    ras 加密[公钥加密]
    :param key: 无BEGIN PUBLIC KEY头END PUBLIC KEY尾的pem格式key
    :param content:待加密内容
    :return:
    """
    pub_key = handle_pub_key(key)
    pub = RSA.import_key(pub_key)
    cipher = PKCS1_v1_5.new(pub)
    encrypt_bytes = cipher.encrypt(content.encode(encoding='utf-8'))
    result = base64.b64encode(encrypt_bytes)
    result = str(result, encoding='utf-8')
    return result


#图片验证码识别
def baiduOCR(picfile):  # picfile:图片文件名
    # 百度提供
    """ 你的 APPID AK SK """
    APP_ID = '22450264'  # 这是你产品服务的appid
    API_KEY = 'HNvLOFnp3rTLpz6Mx8Ge0gIk'  # 这是你产品服务的appkey
    SECRET_KEY = 'hB7dCGcDNd0Z0Iu7Ws6qfjYBpuGWFel7'  # 这是你产品服务的secretkey
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    i = open(picfile, 'rb')
    img = i.read()
    """ 调用通用文字识别（高精度版） """
    message = client.basicAccurate(img)
    i.close()

    # 输出文本内容
    for text in message.get('words_result'):  # 识别的内容
        t=text.get('words')
        s=t.replace(" ", "")
        print(s)
        return s


#获取验证码图片保存到本地
def getFile():
    base_url = 'http://ales.pre.icinfo.co'
    browser = webdriver.Chrome()
    browser.maximize_window()
    browser.implicitly_wait(10)
    browser.get(base_url)
    # (1)登录页面截图
    browser.save_screenshot("F:/Test_Web/Attachments/pic.png")#可以修改保存地址
    time.sleep(2)
    # (3)获取图片验证码坐标
    code_ele = browser.find_element_by_xpath("//img[@class='capcha']")
    # (4)图片4个点的坐标位置
    left = code_ele.location['x']#x点的坐标
    top = code_ele.location['y']#y点的坐标
    right = code_ele.size['width']+left#上面右边点的坐标
    down = code_ele.size['height']+top#下面右边点的坐标
    image = Image.open('F:/Test_Web/Attachments/pic.png')
    # (4)将图片验证码截取
    code_image = image.crop((left, top, right,down))
    code_image.save('F:/Test_Web/Attachments/pic1.png')#截取的验证码图片保存为新的文件
    # 加载图片
    im = Image.open('F:/Test_Web/Attachments/pic1.png')
    # 要先转成灰度图然后才能二值化
    img2 = im.convert('L')
    img2.save('F:/Test_Web/Attachments/pic1.png')
    # 设置一个转换的阈值
    threshold = 80
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    bim = img2.point(table, '1')
    browser.close()  # 关闭页面
    browser.quit()  # 关闭浏览器进程
    return True


#读取excel
class OpeExcel:
    def __init__(self,file_name=None,sheet_id=None):
        if file_name:
            self.file_name = file_name
            self.sheet_id = sheet_id
        else:
            self.file_name = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..\\Attachments\\interface.xlsx"))
            self.sheet_id = 0
        self.data = self.get_data()
    #获取sheets的内容
    def get_data(self):
        data = xlrd.open_workbook(self.file_name)
        tables = data.sheets()[self.sheet_id]
        return tables
    #获取单元格行数
    def get_lines(self):
        tables = self.data
        return tables.nrows
    #获取单元格数据
    def get_value(self,row,col):
        return self.data.cell_value(row,col)


#连接Mysql数据库
class MysqlConnect(object):
    # 魔术方法, 初始化, 构造函数
    def __init__(self,host=Global.DbIp, user=Global.DbUser, password=Global.DbPass, database=Global.DbInstance,port=Global.Port):
        '''
        :param host: IP
        :param user: 用户名
        :param password: 密码
        :param port: 端口号
        :param database: 数据库名
        :param charset: 编码格式
        '''
        self.db = pymysql.connect(host=host, user=user, password=password,port=port, database=database, charset='utf8')
        self.cursor = self.db.cursor()
    # 将要插入的数据写成元组传入
    def exec_data(self, sql, data=None):
        # 执行SQL语句
        self.cursor.execute(sql, data)
        # 提交到数据库执行
        self.db.commit()
    # sql拼接时使用repr()，将字符串原样输出
    def exec(self, sql):
        self.cursor.execute(sql)
        # 提交到数据库执行
        self.db.commit()
    def select(self,sql):
        self.cursor.execute(sql)
        # 获取所有记录列表
        results = self.cursor.fetchall()
        for row in results:
            print(row)
    # 魔术方法, 析构化 ,析构函数
    def __del__(self):
        self.cursor.close()
        self.db.close()

