import allure
from CONFIG.Define import LogLevel
from CONFIG import Global
from common.log import Logger


logger = Logger(logger='BasePage').getlog()

#case公共类和函数
class LogIn():

    def __init__(self, s, host="http://59.202.63.108:80"):
        self.host = host
        self.s = s

    @allure.step("行政执法系统登录")
    def login(self, name="15868385402",
              password="HE6EYw/5NqbZXPVtZxO5Pc8MeZ0r6DaOfYUoz/1yAl5R94EN5lefKKa8jNqpWD9i7Vb82w5iM5z/5XabcEPXNXL0brJ/4ioZo/MCMQN8451TuhUBcb164tRUKmlVi17ORQB/eulsuMX9fO733adaxC5bBrS+T1AZLcyGouBbw5zLa1RUmlBkaXBAP513IaI4pEbB7YiaEJwF5MP2ql4923JPwtJ8uLR4ADjCjgImQTZ5B3wTJv0oKZ5yFhUn0sBOz5oGSRS8YWFkgf2cPH00P0VgcAQFguhtX6L8ij3GLBuxSbb8FgOBPZf43Gdcm1EIb6kkB390+FDQibd/PMGjxQ=="):
        url = self.host + "/api/v2/auth/users/login?_allow_anonymous=true"
        data = {
            "loginName": name,
            "password": password,
            "type": 2,
            "checkCode": "1"
        }
        r = self.s.post(url=url, json=data)
        # 取出 token
        if r.json()['code'] == 200:
            token = r.json()["data"]["token"]
            headers = {
                'Authorization': "Bearer %s" % token,
                'User - Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
            }
            # 更新 headers
            self.s.headers.update(headers)  # 更新到session会话
            logger.info('get token %s' % token)
            return token
        else:
            print("登入失败，启动第二方案写死token（可能过期需要手动填写），失败原因：%s" % r.json())
            token = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJjaGVua2FpIiwiYXVkIjoid2ViIiwiY3JlYXRlZCI6MTYwMTE4OTU1MjA4MywiYXBwSWQiOm51bGwsImlzcyI6ImljaW5mby5jbiIsImV4cCI6MTYwMTc5NDM1Mn0.jYXmXvyIHYIjGmU3Xnjm3zoYwvbeesEf-B4QDcpWWCQxyfNNQh7NNlbAufTyIc3gweG-DQOprVkAcEFAT8RZ0g"
            headers = {
                'Authorization': "Bearer %s" % token,
                'User - Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
            }
            # 更新 headers
            self.s.headers.update(headers)  # 更新到session会话
            logger.info('get token %s' % token)
            return token



# if __name__ == '__main__':
#     s = requests.session()# 会话  代码里面的浏览器，模拟浏览器的功能
#     re = Login(s)
#     r = re.login()
#     print(r)

