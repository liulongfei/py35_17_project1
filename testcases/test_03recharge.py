"""
充值的前提--》提取token
unittest
用例级别的前置：setup
测试类级别的前置：setupclass
"""

import unittest
import os
import requests
from jsonpath import jsonpath
from unittestreport import ddt, list_data
from common.handle_excel import ExcelHandle
from common.handle_path import DATA_DIR
from common.handle_conf import conf
from common.handle_log import my_log
from common.handle_mysql import HandleDB
from common.tools import replace_data
from testcases.fixture import BaseTest


@ddt
class TestRecharge(unittest.TestCase,BaseTest):
    excel = ExcelHandle(os.path.join(DATA_DIR, 'apicases.xlsx'), 'recharge')
    cases = excel.read_data()
    db = HandleDB()

    @classmethod
    def setUpClass(cls):
        """用例类的前置方法：登陆提取token"""
        # 请求登录接口，进行登录
        cls.user_login()

    @list_data(cases)
    def test_recharge(self, item):
        # 第一步准备数据
        url = conf.get('env', 'base_url') + item['url']
        # *******************************动态替换参数***************************************
        # 动态处理需要替换的参数
        # item['data'] = item['data'].replace('#member_id#', str(self.member_id))
        # print(item['data'])
        item['data'] = replace_data(item['data'], TestRecharge)
        params = eval(item['data'])
        # *******************************************************************************

        expected = eval(item['expected'])
        method = item['method'].lower()
        # 第二步发送请求，获取接口的实际返回结果
        # &&&&&&&&&&&&&&请求接口之前查询用户的余额&&&&&&&&&&&&&&&&&&&&

        sql = 'select leave_amount FROM futureloan.member WHERE mobile_phone="{}"'.format(
            conf.get('test_data', 'mobile'))
        start_amount = self.db.find_one(sql)[0]
        print('用例执行前的余额', start_amount)
        response = requests.request(method=method, url=url, json=params, headers=self.headers)
        res = response.json()
        print('预期结果', expected)
        print('实际结果', res)
        # &&&&&&&&&&&&&&请求接口之后查询用户的余额&&&&&&&&&&&&&&
        end_amount = self.db.find_one(sql)[0]
        print('用例执行后的余额', end_amount)

        # 第三步断言
        try:
            self.assertEqual(expected['code'], res['code'])
            self.assertEqual(expected['msg'], res['msg'])
            # &&&&&&&&&&&&&&校验数据库中用户金额的变化是否等于充值金额&&&&&&&&&&&&&&#
            if res['msg'] == 'OK':
                # 充值成功，用户余额的变化为充值金额
                self.assertEqual(float(end_amount - start_amount), params['amount'])
            else:
                # 充值失败用户余额变化为0
                self.assertEqual(float(end_amount - start_amount), 0)
        except AssertionError as e:
            my_log.error('用例--【{}】--失败'.format('title'))
            my_log.exception(e)
            raise e
        else:
            my_log.info('用例--【{}】--成功'.format('title'))
