import pymysql

# 1.链接数据库
con = pymysql.connect(host='api.lemonban.com',
                      port=3306,
                      user='future',
                      password='123456',
                      charset='utf8'
                      # cursorclass=pymysql.cursors.DictCursor
                      )

with con as cur:
    sql = 'select * FROM futureloan.member LIMIT 5;'
    res = cur.execute(sql)

print(res)
# res = cur.fetchall()
result = cur.fetchone()
print(result)
cur.close()
con.close()

# print(con)
# # 2.创建游标对象
# cur=con.cursor()
# sql=''
# #3.执行sql语句
# cur.execute(sql)
# cur.con.commit()
# cur.close()
# con.close()
