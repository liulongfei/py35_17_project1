import os
import unittest
import requests
import jsonpath
from unittestreport import ddt, list_data
from common.handle_excel import ExcelHandle
from common.handle_path import DATA_DIR
from common.handle_conf import conf
from common.handle_log import my_log


@ddt
class Test_Recharge(unittest.TestCase):
    excel = ExcelHandle(os.path.join(DATA_DIR, 'apicases.xlsx'), 'recharge')
    cases = excel.read_data()

    @classmethod
    def setUpClass(cls) -> None:
        url = conf.get('env', 'base_url') + 'member/login'
        params = {
            "mobile_phone": conf.get('test_data', 'mobile'),
            "pwd": conf.get('test_data', 'pwd')
        }
        headers = eval(conf.get('env', 'headers'))
        response = requests.post(url=url, json=params, headers=headers)
        res = response.json()
        # print(res)
        token = jsonpath(res, '$..token')[0]
        print(token)
        headers['Authorization'] = 'Bearer ' + token
        cls.headers = headers
        cls.member_id=jsonpath(res,'$..id')[0]
        print(cls.member_id)
        # setattr(Test_Recharge,'headers',headers)

    @list_data(cases)
    def test_recharge(self, item):
        url = conf.get('env', 'base_url') + item['url']
        item['data'] = item['data'].replace('#member_id#', str(self.member_id))
        # print(item['data'])
        params = eval(item['data'])
        expected = eval(item['expected'])
        method = item['method'].lower()
        response = requests.request(method=method, url=url, json=params, headers=self.headers)
        print(response.json())
        try:
            self.assertEqual(expected['code'], response['code'])
            self.assertEqual(expected['msg'], response['msg'])
        except AssertionError as e:
            my_log.error('用例--【{}】--失败'.format('title'))
            my_log.exception(e)
            raise e
        else:
            my_log.info('用例--【{}】--成功'.format('title'))


