import re


def replace_data(data, cls):
    """
    :param data: 要进行替换的用例数据(字符串)
    :param cls: 测试类
    :return:
    """
    while re.search('#(.+?)#', data):
        res2 = re.search('#(.+?)#', data)
        item = res2.group()
        attr = res2.group(1)
        value = getattr(cls, attr)
        # 进行替换
        data = data.replace(item, str(value))

    return data