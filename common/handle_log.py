# -*- coding: utf-8 -*-
# @TIME     :2021/1/14 10:48
# @Author   :Hachi
# @Email    :459327366@qq.com
# @File     :handle_log.py
# @Software :PyCharm

import logging
import os
from common.handle_conf import conf
from common.handle_path import LOG_DIR


def create_log(name='my_log', level='DEBUG', filename='log.log', fh_level='DEBUG', sh_level='DEBUG'):
    # 第一步创建日志收集器
    log = logging.getLogger(name)
    #     第二步设置日志收集器日志等级
    log.setLevel(level)
    #    第三步设置日志输出渠道
    # 3.1.输出到文件的配置
    fh = logging.FileHandler(filename, encoding='utf-8')
    fh.setLevel(fh_level)
    log.addHandler(fh)
    # 3.2.输出到控制台
    sh = logging.StreamHandler()
    sh.setLevel(sh_level)
    log.addHandler(sh)

    # 四.设置日志输出的格式
    # 4、设置日志输出的等级
    formats = '%(asctime)s - %(filename)s-->line:%(lineno)d] - %(levelname)s: %(message)s'
    # 创建格式对象
    log_format = logging.Formatter(formats)
    # 设置输出到控制台的日志格式
    sh.setFormatter(log_format)
    fh.setFormatter(log_format)
    # 设置输出到文件的日志格式
    # log_format2 = logging.Formatter('%(asctime)s--%(levelname)s:%(message)s')
    # 返回一个日志收集器
    return log


my_log = create_log(
    name=conf.get("logging", 'name'),
    level=conf.get('logging', 'level'),
    filename=os.path.join(LOG_DIR,conf.get("logging", 'filename')),
    sh_level=conf.get('logging', 'sh_level'),
    fh_level=conf.get('logging', 'fh_level')
)
