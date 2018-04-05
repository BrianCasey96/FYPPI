import temp
import moisture_level
import sendAllData
import unittest
import pymysql.cursors
import config

user = config.user()
passwd = config.returnPassword()
db = config.db()


class TestCases(unittest.TestCase):

	#Checks that the moisture, temp and light readings are not nil
    def test_mositure_level(self):
	adc_output, percent = moisture_level.reading()
    	self.assertIsNotNone(adc_output)
	self.assertIsNotNone(percent)

    def test_temp_reading(self):
	x = temp.read_temp()
	self.assertIsNotNone(x)

#    def test_light_reading(self):
#	self.assertIsNotNone(sendAllData.lightPercentage)

    def test_values_sent(self):
	#imports the sendValues function from sendAllDate
	sendAllData.sendValues(70, 21.50, 87)
	print("Sending values 70, 21.50 and 87")
	cnx = pymysql.connect(host = "127.0.0.1",
			      user = user,
			      passwd = passwd,
			      db = db,
			      port = 3307)

	with cnx.cursor() as cursor:
		result = cursor.execute("select moisture from pidata order by time_value desc LIMIT 1")
		print(result)
		moisture = cursor.fetchone()
		self.assertEqual((70,) , moisture)

		result = cursor.execute("select light from pidata order by time_value desc LIMIT 1")
                print(result)
                light  = cursor.fetchone()
                self.assertEqual((87,) , light)

		result = cursor.execute("select temp from pidata order by time_value desc LIMIT 1")
                print(result)
                temp = cursor.fetchone()
                self.assertEqual((21.50,) , temp)


def main():
    unittest.main()

if __name__ == "__main__":
    main()
