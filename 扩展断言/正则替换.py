import re


class TestData:
    id = 123
    name = 'musen'
    data = '1122'
    title = '测试数据'


s = '{"id": "#id#", "name": "#name#", "data": "#data#", "title": "#title#", "aaa": 11, "bbb": 222}'

while re.search('#(.+?)#', s):
    res2 = re.search('#(.+?)#', s)
    item = res2.group()
    attr = res2.group(1)
    value = (getattr(TestData, attr))
    s = s.replace(item, str(value))
print(s)
