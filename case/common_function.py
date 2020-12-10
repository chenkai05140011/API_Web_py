import allure
from CONFIG.Define import LogLevel
from COMMON import Log
from CONFIG import Global

#case公共类和函数
class LogIn():

    def __init__(self, s, host="http://59.202.63.108:80"):
        self.host = host
        self.s = s

    @allure.step("行政执法系统登录")
    def login(self, name="15868385402",
              password="AY1qyA+eyDFnxkplZIOBnkFpaLKr2kjgkQZ+l0wvHndMSxFtZJjpDxxNiMMXuzC7x0xj3J8lxCpPlnf+QK1eqM+lpaoIlL8r0keTZXsbfpAKl3Gtn+oZ38Iv7o1ROPjTxU8XNQOj+TkLgl8LWhoK/3Oj3FpyZlZE8+87PWnajZG5ua3U5zGQ2Eud8MRSu7Rb+mmXJ81WDM5za6Xft4WrLJXtIALeua8ZZTi6vv3/BUEi+7x3fIMMfDmGGUNI43P1//s11Rl4EFm4OiLnp0tiz3HbtjqiSewBN/hm36kY7yZNkLKWXXa20pFYA1wyEu65xzpgReX/AcCcOwSMMdAxNQ=="):
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
            return token

# if __name__ == '__main__':
#     s = requests.session()# 会话  代码里面的浏览器，模拟浏览器的功能
#     re = Login(s)
#     r = re.login()
#     print(r)

