import sqlite3,pymysql
import pandas

'''

readme:这个文件仅仅是录入了sql的一些简单的数据库操作,
对于日常使用有少量帮助(复制粘贴嘛)

'''


a = sqlite3.connect('src/plugins/plugins/test.db')
b = a.cursor()
#执行SQL语句

#建立表的列名
# b.execute('create table user(id int(10) primary key,name varchar(20))')

# sql = 'insert into user (id,name) values(?,?)'
# b.execute(sql,(77,'hhh'))#写入上面对应位置值

# sql = 'insert into user (id,name) values(?,?)'
# 数据 = [(1,'11'),(2,'222'),(3,'333'),(4,'444')]
# b.executemany(sql,数据)#插入对应的值

# sql = 'select "2" from user'
# b.execute(sql)
# 结果 = b.fetchone()#查询对应的下一条结果
# print(结果)

# sql = "select * from user"
# b.execute(sql)
# for i in range(0,9):
#     结果 = b.fetchone()[0]
#     print(结果)

# sql = 'select * from user where id > 3'
# b.execute(sql)
# 结果 = b.fetchall()
# print(结果)

# sql = 'select * from user order by id'
# b.execute(sql)
# sql = 'select * from user where id > 3'
# b.execute(sql)
# sql = 'select * from user where name > 555 and id > 3'
# b.execute(sql)
# 结果 = b.fetchall()
# print(结果)

# sql = 'update user set name = ? where id == ?'
# b.execute(sql,('name','id'))

# sql = 'delete from user where id = ?'
# b.execute(sql,(2,))

# sql = 'delete from user'
# b.execute(sql)

# b.execute('''create table notice(time real,id text,notice text,mod int)''')

# c = b.execute('SHOW TABLES')
# print(c.fetchall())

b.close()
a.commit()
a.close()

