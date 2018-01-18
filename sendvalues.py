import MySQLdb
import datetime
cnx = MySQLdb.connect(host="sql2.freemysqlhosting.net",
					  user="sql2202637",
					  passwd="aI7%wK3%",
					  db="sql2202637")

cur = cnx.cursor()


light = 5
moisture = 93
temp = 22.50



sql = "INSERT INTO Date_and_Value VALUES (null, '%d', '%lf', '%d' )" % (moisture, temp, light)
cur.execute(sql)

cur.execute("INSERT INTO `Test` (`Number`) VALUE('11')")
cnx.commit()

cur.execute("SELECT * FROM Test")

for row in cur.fetchall():
    print(row[0])

cnx.close()

