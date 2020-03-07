import pymysql


conx= pymysql.connect(host="localhost",user="root",passwd="",db="login")
myCursor=conx.cursor()

myCursor.execute(""" INSERT INTO users (username,password) VALUES ('emna','5678');""")
conx.commit()
result = myCursor.execute("SELECT * FROM users")
conx.close()
