import temp
import moisture_level
import sendAllData
import unittest
import pymysql.cursors

class LearningCase(unittest.TestCase):
    def test_starting_out(self):
        self.assertEqual(1, 1)

    def test_mositure_level(self):
	adc_output, percent = moisture_level.reading()
    	self.assertIsNotNone(adc_output)
	self.assertIsNotNone(percent)

    def test_temp_reading(self):
	x = temp.read_temp()
	self.assertIsNotNone(x)

    def test_values_sent(self):
	sendAllData.sendValues(70, 21.50, 87)
	cnx = pymysql.connect(host = "127.0.0.1",
			      user = "brian",
			      passwd = "butterfly",
			      db = "plant_data",
			      port = 3307
)
	with cnx.cursor() as cursor:
		result = cursor.execute("select * from pidata order by time_value desc LIMIT 1")
		print(result)
		print(cursor.fetchone())

def main():
    unittest.main()

if __name__ == "__main__":
    main()
