# -*- coding: utf-8 -*-
# @TIME     :2021/1/17 7:04
# @Author   :Hachi
# @Email    :459327366@qq.com
# @File     :handle_patn.py
# @Software :PyCharm

import os

# 项目根目录绝对路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 用例数据所在目录
DATA_DIR = os.path.join(BASE_DIR, 'datas')
# 配置文件所在目录
CONF_DIR = os.path.join(BASE_DIR, 'conf')
# 日志文件所在目录
LOG_DIR = os.path.join(BASE_DIR, 'logs')
# 报告所在目录
REPORT_DIR = os.path.join(BASE_DIR, 'reports')
# 用例模块所在目录
CASES_DIR = os.path.join(BASE_DIR, 'testcases')
