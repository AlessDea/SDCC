import mysql.connector

from mysql.connector import Error

def connect_mysql():
	try:
		connection = mysql.connector.connect(host='localhost', port='3306', database='mydb', user='root', password='password')
		if connection.is_connected():
		    db_Info = connection.get_server_info()
		    print("Connected to MySQL Server version ", db_Info)
		    cursor = connection.cursor()
		    cursor.execute("select database();")
		    record = cursor.fetchone()
		    print("You're connected to database: ", record)
		    return connection

	except Error as e:
		print("Error while connecting to MySQL", e)
	
	


def query1(c):
	mycursor = c.cursor()
	sql = 'INSERT INTO user VALUES (%s, %s, %s)'
	val = ('franco', 'franco@email.it', 'cazzone')
	mycursor.execute(sql, val)
	
	c.commit()
	
	
def query2(c):
	mycursor = c.cursor()
	sql = 'SELECT * FROM user'	
	
	mycursor.execute(sql)
	
	myresult = mycursor.fetchall()
	
	for res in myresult:
		print(res)
	



if __name__ == '__main__':
	conn = connect_mysql()
	# query2(conn)
	# query1(conn)
	query2(conn)
	print('finished')
	conn.close()
