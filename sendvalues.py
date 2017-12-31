import MySQLdb
cnx = MySQLdb.connect(host="sql2.freemysqlhosting.net",
					  user="sql2202637",
					  passwd="aI7%wK3%",
					  db="sql2202637")

cur = cnx.cursor()

num = 5
sql = "INSERT INTO Test(Number) VALUE ('%d' )" % (num)
cur.execute(sql)

cur.execute("INSERT INTO `Test` (`Number`) VALUE('11')")
cnx.commit()

cur.execute("SELECT * FROM Test")

for row in cur.fetchall():
    print(row[0])

cnx.close()

