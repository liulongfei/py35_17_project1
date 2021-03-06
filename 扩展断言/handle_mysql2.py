import pymysql
from common.handle_conf import conf


class HandleDB:
    def __init__(self):
        self.con = pymysql.connect(host=conf.get('mysql', 'host'),
                                   port=conf.getint('mysql', 'port'),
                                   user=conf.get('mysql', 'user'),
                                   password=conf.get('mysql', 'password'),
                                   charset='utf8'
                                   # cursorclass=pymysql.cursors.DictCursor
                                   )

    def find_all(self, sql):
        # sql 获取查询所有数据
        with self.con as cur:
            cur.execute(sql)
        res = cur.fetchall()
        cur.close()
        return res

    def find_one(self, sql):
        # 查询第一条数据
        with self.con as cur:
            cur.execute(sql)
        res = cur.fetchone()
        cur.close()
        return res

    def find_count(self, sql):
        # sql 执行完后返回的数据条数
        with self.con as cur:
            res = cur.execute(sql)
        cur.close()
        return res

    def __del__(self):
        self.con.close()


if __name__ == '__main__':
    sql = 'select * FROM futureloan.member LIMIT 5;'
    db = HandleDB()
    # res = db.find_one(sql)
    # res=db.find_count(sql)
    res = db.find_all(sql)
    print(res)
    del db
