# -- coding:UTF-8 --
#登录参数（用户名、密码、验证码等）
UserInfo = {"loginName":"15868810134",
            "password":"kOBMeWA9EegzDwb3bRO5uEEevpCEQvTmAYk2jJ0sUly/Ty1oVymgZ6As98b7K1OfTmE70IsM51rwd5zKLiP6Y+cB/0V5SQNCz3DJ3df3JhasB9KHN2ZJENx82a2Snr4Pho12fSekHk8uoZ0/OhG+aGsvInims7JNgtrvlPNC6ptf0yGBtvs7taPKjRfVC9rVkKfDL/jzbJmiSJcIbUDfa0sGdOwkpSZ+3SmYssJBobpL+601wDYMALOVWj5YLK36Ly/ebiJHXaO14FNFIlygQUTd5SZDj5XTSnrSmepbpsKrteOoxZIkQbj8GXLIHvxjyIPC07mc3Uo8S3NS6cAGXw==",
            "type":2,
            "checkCode":"11"
            }


#行政执法监管平台PC端ip地址
#测试环境
# JGPC="http://192.168.1.232:9999"
#预发环境
JGPC='http://ales.pre.icinfo.co'
#正式环境
# JGPC='http://59.202.42.163:180/'


#行政执法监管平台PC端登录
#测试环境
# LoginUrlPC="http://192.168.1.232:9999/api/v2/auth/users/login?_allow_anonymous=true"
#预发环境
# LoginUrlPC="http://ales.pre.icinfo.co/api/v2/auth/users/login?_allow_anonymous=true"
#正式环境
# LoginUrlPC="http://59.202.42.163:180/admin/jump_verifyUser"


#行政执法监管平台测试环境数据库
DbIp = '192.168.1.254'
DbInstance = 'member_ts' #数据库实例
DbUser = 'member_ts'     #数据库用户
DbPass = 'kyLMBoJ06XXC7k3T' #数据库密码
Port = 3306



class responseClass():
    result = None
    statusLine = None
    text = None
    content = None