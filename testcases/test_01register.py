import unittest
import os
import random
import requests
from unittestreport import ddt, list_data
from common.handle_excel import ExcelHandle
from common.handle_path import DATA_DIR
from common.handle_conf import conf
from common.handle_log import my_log
from common.handle_mysql import HandleDB
from common.tools import replace_data


@ddt
class TestRegister(unittest.TestCase):
    excel = ExcelHandle(os.path.join(DATA_DIR, 'apicases.xlsx'), 'register')
    cases = excel.read_data()
    base_url = conf.get('env', 'base_url')
    print(base_url)
    headers = eval(conf.get('env', 'headers'))
    db = HandleDB()

    @list_data(cases)
    def test_register(self, item):
        # 第一步准备用例数据
        # 接口地址
        url = self.base_url + item['url']
        # phone = self.random_mobile()
        # item['data'] = item['data'].replace('#mobile#', phone)
        #
        # 接口请求参数
        # 判斷是否有手机号需要替换
        if '#mobile#' in item['data']:
            # phone = self.random_mobile()
            setattr(TestRegister,'mobile',self.random_mobile())
        item['data'] = replace_data( item['data'], TestRegister)
        params = eval(item['data'])
        # 请求头
        # 获取请求方法并转换为小写
        method = item['method'].lower()
        # 用例预期结果
        expected = eval(item['expected'])
        # 第二步请求接口，获取实际结果
        # requests.post(url=url,json=params,headers=self.headers)
        response = requests.request(method, url, json=params, headers=self.headers)
        res = response.json()
        # 查询该数据库中该手机号对应的账户数量
        sql = 'select * FROM futureloan.member WHERE mobile_phone="{}"'.format(params.get('mobile_phone', ""))
        count = self.db.find_count(sql)
        # 第三步 断言
        print('预期结果', expected)
        print('实际结果', res)
        try:
            self.assertEqual(expected['code'], res['code'])
            self.assertEqual(expected['msg'], res['msg'])
            if item['check_sql']:
                print('数据库中查询的数量为：', count)
                self.assertEqual(1, count)

        except AssertionError as e:
            my_log.error('用例---【{}】---执行失败'.format(item['title']))
            my_log.exception(e)
            # my_log.error(e)
            # 回写结果到Excel
            raise e
        else:
            my_log.info('用例---【{}】---执行通过'.format(item['title']))

    def random_mobile(self):
        """随机生成手机号"""

        phone = str(random.randint(18800000000, 18899999999))
        return phone
        # mobile = '133'
        # for i in range(8):
        #     n = str(random.randint(0, 9))
        #     mobile += n
