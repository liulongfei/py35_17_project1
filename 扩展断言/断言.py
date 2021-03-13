import unittest
class TestDemo(unittest.TestCase):
    def test_demo(self):
        res = {'code': 0, 'msg': 'ok', 'time': '20201212'}
        expected = {'code': 0, 'msg': 'ok'}
        self.assertDictIn(expected,res)
    def assertDictIn(self, expected, res):
        for k, v in expected.items():
            if res.get(k) == v:
                print(k, v, 'res找到了这个值')
            else:
                raise AssertionError('{}[k,v] not in{}'.format(expected, res))

# res = {'code': 0, 'msg': 'ok', 'time': '20201212'}
# expected = {'code': 0, 'msg': 'ok'}


