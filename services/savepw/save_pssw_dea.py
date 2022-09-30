import mysql.connector
import logging

from mysql.connector import Error

from services.savepw import savepwd_pb2_grpc, savepwd_pb2




def connect_mysql():

    try:
        connection = mysql.connector.connect(host='login-db', port='6666', database='mydb', user='root',
                                             password='')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
            return connection

    except Error as e:
        return None

def save(uname, pw, service, sql_conn):
    mycursor = sql_conn.cursor()

    check_query = "SELECT COUNT(*) FROM private_passwords WHERE username = %s AND service = %s"
    val = (uname, service)
    mycursor.execute(check_query, val)

    myresult = mycursor.fetchone()[0]
    if(myresult != None):
        # do the insert
        query1 = 'INSERT INTO private_passwords VALUES (%s, %s, %s)'
        val = (uname, pw, service)
        mycursor.execute(sql, val)
    else:
        # do the update
        query2 = 'UPDATE private_passwords SET password = %s WHERE username = %s AND service = %s'
        val = (pw, uname, service)
        mycursor.execute(sql, val)

    sql_conn.commit()
    sql_conn.close()



class Saver(savepwd_pb2_grpc.SaverServicer):

    def SavePw(self, request, context):
        ret = save(request.username, request.pw, request.service)
        if ret:
            return savepwd_pb2.SaveReply(message='Success')
        return savepwd_pb2.SaveReply(message='Error')

