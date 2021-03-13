import re
# s = 'GO is  234python234 java'
# res = re.findall(r'python\B',s)
# print(res)

# print('python \bjava')

s = '{"id": "#id#", "name": "#name#", "data": "#data#", "title": "#title#", "aaa": 11, "bbb": 222}'

# findall:匹配字符串中所有符合规则的数据并以列表的形式返回
res = re.findall('#(.+?)#', s)
print(res)

