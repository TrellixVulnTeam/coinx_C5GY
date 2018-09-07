import numpy
import iota_eth.robot_fun
import time
import yaml
import random
import config.dbUtil

f = open('config/basic_cfg.yaml')
data = yaml.load(f)

#登录地址
url_login = data['loginUrl']

#挂单地址
url_order = data['orderUrl']

#获取最新交易价格
iota_eth_url = data['coinmarket'] + str(1720) + '/?convert=eth'

#用户账号密码

tester01 = data['count']['tester01']
password1 = data['count']['password1']

tester02 = data['count']['tester02']
password2 = data['count']['password2']

token01 = iota_eth.robot_fun.get_access_token(url_login, tester01, password1)
token02 = iota_eth.robot_fun.get_access_token(url_login, tester02, password1)

tradePairCode = 'iota_eth'

while 1:
    try:
        iota_eth_lastprice = float(iota_eth.robot_fun.getMarketPrice(iota_eth_url))
        sql = "insert into coin (name,price) values ('iota',%f);" % iota_eth_lastprice
        config.dbUtil.execute(sql)

    except Exception as e:
        continue

    nowTime = time.time()

    for i in range(1,1000000):
        count1 = round(random.uniform(1, data['tradePair']['iota_ethMaxCount']), 0)
        req1 = iota_eth.robot_fun.order_buy(tester01, iota_eth_lastprice, url_order, token01, tradePairCode, count1)
        #设置等待时间
        if round(nowTime) % random.randint(1, i + 2):
            time.sleep(random.uniform(0, 5))
        else:
            time.sleep(numpy.random.random(5)[random.randint(0, 4)] + 0.5)

        count2 = round(random.uniform(1, data['tradePair']['iota_ethMaxCount']), 0)
        req2 = iota_eth.robot_fun.order_sell(tester02, iota_eth_lastprice, url_order, token02, tradePairCode, count2)
        #设置等待时间
        if round(nowTime) % random.randint(1, i + 2):
            time.sleep(random.uniform(0, 5))
        else:
            time.sleep(numpy.random.random(5)[random.randint(0, 4)] + 0.5)

        if req1.json()['msg'] == 'AccessToken已过期':
            iota_eth.robot_fun.get_access_token(url_login, tester01, password1)

        if req2.json()['msg'] == 'AccessToken已过期':
            iota_eth.robot_fun.get_access_token(url_login, tester02, password2)

        #30秒后跳出循环重新获取最新交易价格
        runTime = time.time()
        if ((runTime - nowTime) > 60):
            break

