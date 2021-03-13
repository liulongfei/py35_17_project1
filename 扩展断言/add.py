import unittest
import os
import requests
import jsonpath
from unittestreport import ddt, list_data
from common.handle_excel import ExcelHandle
from common.handle_path import DATA_DIR
from common.handle_conf import conf
from common.tools import replace_data
from common.handle_log import my_log

@ddt
class TestAdd(unittest.TestCase):
    excel = ExcelHandle(os.path.join(DATA_DIR, 'apicases.xlsx'), 'add')
    cases = excel.read_data()

    @classmethod
    def setUpClass(cls) -> None:
        url = conf.get('env', 'base_url') + '/member/login'
        params = {
            'mobile_phone': conf.get('test_data', 'mobile'),
            'pwd': conf.get('test_data', 'pwd')
        }
        headers = eval(conf.get('env', 'headers'))
        response = requests.post(url=url, json=params, headers=headers)
        res = response.json()
        token = jsonpath(res,'$..token')[0]
        headers['Authorization'] = 'Bearer ' + token
        cls.headers = headers
        cls.member_id = jsonpath(res,'$..id')

    @list_data(cases)
    def test_add(self, item):
    # 准备数据
        url = conf.get('env', 'base_url') + item['url']
        item['data']=replace_data(item['data'],TestAdd)
        params=eval(item['data'])
        expected=eval(item['expected'])
        method=item['method']
        response=requests.request(method=method,url=url,json=params,headers=self.headers)
        res=response.json()
        try:
            self.assertEqual(expected['code'],res['code'])
            self.assertEqual(expected['msg'],res['msg'])
        except AssertionError as e:
            my_log.error('用例--【{}】---执行失败'.format(item['title']))
            my_log.exception(e)
            raise e
        else:
            my_log.info('用例--【{}】---执行成功'.format(item['title']))


