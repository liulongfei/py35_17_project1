import unittest
import os

import requests
from jsonpath import jsonpath
from unittestreport import ddt, list_data

from common.handle_conf import conf
from common.handle_excel import ExcelHandle
from common.handle_log import my_log
from common.handle_path import DATA_DIR
from testcases.fixture import BaseTest
from common.tools import replace_data
from common.handle_mysql import HandleDB


@ddt
class TestInvest(unittest.TestCase, BaseTest):
    excel = ExcelHandle(os.path.join(DATA_DIR, 'apicases.xlsx'), 'invest')
    cases = excel.read_data()
    db=HandleDB()

    @classmethod
    def setUpClass(cls) -> None:
        # ------管理员登录——————
        cls.admin_login()
        cls.user_login()
        cls.add_project()
        cls.audit()

    @list_data(cases)
    def test_invest(self, item):
        url = conf.get('env', 'base_url') + item['url']
        item['data'] = replace_data(item['data'], TestInvest)
        params = eval(item['data'])
        expected = eval(item['expected'])
        method = item['method']
        # ----------------投资前查询数据库----------------------------
        #查用户表的sql

        sql1 = 'select leave_amount FROM futureloan.member where id= "{}"'.format(self.member_id)
        # 查投资记录的sql
        sql2 = 'select id FROM futureloan.invest where member_id= "{}"'.format(self.member_id)
        # 查流水记录的sql
        sql3 = 'select id FROM futureloan.financelog where pay_member_id= "{}" '.format(self.member_id)
        if item['check_sql']:
            s_amount=self.db.find_one(sql1)[0]
            s_invest=self.db.find_count(sql2)
            s_financelog=self.db.find_count(sql3)




        response = requests.request(method=method, url=url, json=params, headers=self.headers)
        res = response.json()
        # --------------投资后查询数据库-----------------------------
        if item['check_sql']:
            e_amount=self.db.find_one(sql1)[0]
            e_invest=self.db.find_count(sql2)
            e_financelog=self.db.find_count(sql3)

        try:
            self.assertEqual(expected['code'], res['code'])
            self.assertIn(expected['msg'],res['msg'])
            if item['check_sql']:
                # 断言用户余额
                self.assertEqual(params['amount'],float(s_amount-e_amount))
                # 断言投资记录
                self.assertEqual(1,e_invest-s_invest)
                # 断言流水记录
                self.assertEqual(1,e_financelog-s_financelog)
        except AssertionError as e:
            my_log.error("用例--【{}】---执行失败".format(item['title']))
            my_log.exception(e)
            raise e
        else:
            my_log.info("用例--【{}】---执行通过".format(item['title']))
