import unittest
from unittestreport import TestRunner
from common.handle_path import CASES_DIR, REPORT_DIR
from unittestreport.core.sendEmail import SendEmail


class RunTest():
    def main(self):
        suite = unittest.defaultTestLoader.discover(CASES_DIR)
        runner = TestRunner(suite,
                            filename='py35.html',
                            report_dir=REPORT_DIR,
                            title='测试报告',
                            tester='LF',
                            desc="XX项目测试生成的报告",
                            templates=1
                            )
        runner.run()
        # 将测试结果发到email邮箱
        runner.send_email(host='smtp.qq.com',
                          port=465,
                          user='459327366@qq.com',
                          password='masnywlgdesvbghi',
                          to_addrs='llf459327366@163.com',
                          is_file=True)
        # webhook='https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=293fffcf-5a82-447a-85b1-083148cad4ce'

        # 推送测试结果到企业微信
        # # 方式一：
        # runner.weixin_notice(chatid="企业微信群id", access_token="调用企业微信API接口的凭证")
        # # 方式二：
        # runner.weixin_notice(chatid="企业微信群id", corpid='企业ID', corpsecret='应用的凭证密钥')
        # -----------扩展-------------------
        # em = SendEmail(host='smtp.qq.com',
        #                port=465,
        #                user='459327366@qq.com',
        #                password='masnywlgdesvbghi')
        # em.send_email(subject="测试报告",
        #               content='邮件内容',
        #               filename='feifei',
        #               to_addrs='llf459327366@163.com')


if __name__ == '__main__':
    test = RunTest()
    test.main()
