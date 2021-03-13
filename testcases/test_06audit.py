import unittest
import os
import requests
from jsonpath import jsonpath
from unittestreport import ddt, list_data
from common.handle_excel import ExcelHandle
from common.handle_log import my_log
from common.handle_path import DATA_DIR
from common.handle_conf import conf
from common.tools import replace_data
from common.handle_mysql import HandleDB
from testcases.fixture import BaseTest


@ddt
class TestAudit(unittest.TestCase,BaseTest):
    excel = ExcelHandle(os.path.join(DATA_DIR, 'apicases.xlsx'), 'audit')
    cases = excel.read_data()
    db = HandleDB()

    @classmethod
    def setUpClass(cls) -> None:
        # ------管理员登录——————
        cls.admin_login()

        # ------普通用户登录——————
        cls.user_login()


    def setUp(self) -> None:
        """用例级别的前置:添加项目"""
        self.add_project()



        # setattr(TestAudit,'load_id',jsonpath(res,'$..id')[0])

    @list_data(cases)
    def test_audit(self, item):
        url = conf.get('env', 'base_url') + item['url']
        item['data'] = replace_data(item['data'], TestAudit)
        params = eval(item['data'])
        method = item['method']
        expected = eval(item['expected'])
        response = requests.request(method=method, url=url, json=params, headers=self.admin_headers)
        res = response.json()
        # 判断是否审核通过的用例，且审核成功，如果是则保存项目ID为审核通过的项目ID
        # if res['msg']=='OK' and params['approved_or_not']=='True':
        if res['msg'] == 'OK' and item['title'] == '审核通过':
            TestAudit.pass_loan_id = params['loan_id']
        # 第三步：断言
        print("预期结果:", expected)
        print("实际结果：", res)
        try:
            # 断言code和msg字段是否一致
            self.assertEqual(expected['code'], res['code'])
            self.assertEqual(expected['msg'], res['msg'])
            if item['check_sql']:
                sql = item['check_sql'].format(self.loan_id)
                status = self.db.find_one(sql)[0]
                print('数据库中的状态', status)
                self.assertEqual(expected['status'], status)

        except AssertionError as e:
            # 记录日志
            my_log.error("用例--【{}】---执行失败".format(item['title']))
            my_log.exception(e)
            raise e
        else:
            my_log.info("用例--【{}】---执行通过".format(item['title']))
