import pymysql

connection= pymysql.connect(host="localhost",user="root",passwd="",db="my_python")

myCursor=connection.cursor()
myCursor.execute(""" CREATE TABLE names
(
	id int primary key,
	name varchar(20)
)
""")
connection.commit()
connection.close()