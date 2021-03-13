import unittest
import os
import requests
from unittestreport import ddt, list_data
from common.handle_excel import ExcelHandle
from common.handle_path import DATA_DIR
from common.handle_conf import conf
from common.handle_log import my_log
from common.tools import replace_data


@ddt
class TestLogin(unittest.TestCase):
    excel = ExcelHandle(os.path.join(DATA_DIR, 'apicases.xlsx'), 'login')
    cases = excel.read_data()
    base_url = conf.get('env', 'base_url')
    headers = eval(conf.get('env', 'headers'))

    @list_data(cases)
    def test_login(self, item):
        url = self.base_url + item['url']
        item['data'] = replace_data(item['data'], TestLogin)
        params = eval(item['data'])
        method = item['method'].lower()
        expected = eval(item['expected'])
        response = requests.request(method, url, json=params, headers=self.headers)
        res = response.json()
        try:
            # self.assertEqual(expected['code'], res['code'])
            # self.assertEqual(expected['msg'], res['msg'])
            self.assertDictIn(expected, res)
        except AssertionError as e:
            my_log.error('用例---【{}】---执行失败'.format(item['title']))
            # my_log.exception(e)
            raise e
        else:
            my_log.info('用例---【{}】---执行通过'.format(item['title']))

    def assertDictIn(self, expected, res):
        for k, v in expected.items():
            if res.get(k) == v:
                pass
            else:
                raise AssertionError('{}[k,v] not in{}'.format(expected, res))
