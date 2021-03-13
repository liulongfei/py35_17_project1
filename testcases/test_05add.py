import unittest
import os
import requests
from jsonpath import jsonpath
from unittestreport import ddt, list_data
from common.handle_excel import ExcelHandle
from common.handle_path import DATA_DIR
from common.handle_conf import conf
from common.tools import replace_data
from common.handle_log import my_log
from common.handle_mysql import HandleDB
from testcases.fixture import BaseTest


@ddt
class TestAdd(unittest.TestCase,BaseTest):
    excel = ExcelHandle(os.path.join(DATA_DIR, 'apicases.xlsx'), 'add')
    cases = excel.read_data()
    db = HandleDB()

    @classmethod
    def setUpClass(cls) -> None:
       #  前置登录
       cls.user_login()

    @list_data(cases)
    def test_add(self, item):
        # 准备数据
        url = conf.get('env', 'base_url') + item['url']
        item['data'] = replace_data(item['data'], TestAdd)
        params = eval(item['data'])
        expected = eval(item['expected'])
        method = item['method']
        sql='select * from futureloan.loan where member_id={}'.format(self.member_id)
        start_count = self.db.find_count(sql)
        print('调用之前项目个数',start_count)
        response = requests.request(method=method, url=url, json=params, headers=self.headers)
        res = response.json()
        end_count=self.db.find_count(sql)
        print('调用之后项目个数',end_count)
        try:
            self.assertEqual(expected['code'], res['code'])
            self.assertEqual(expected['msg'], res['msg'])
            #根据添加项目是否成功，来对数据库进行分别校验
            if res['msg']=='OK':
                self.assertEqual(end_count-start_count,1)
            else:
                self.assertEqual(end_count-start_count,0)

        except AssertionError as e:
            my_log.error('用例--【{}】---执行失败'.format(item['title']))
            my_log.exception(e)
            raise e
        else:
            my_log.info('用例--【{}】---执行成功'.format(item['title']))
