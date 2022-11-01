import mysql
import mysql.connector



def connect_mysql():

    connection = mysql.connector.connect(
        #host="groups-db",
        host='localhost',
        user="root",
        password="",
        database="mydb",
        port="3306"
        #auth_plugin='mysql_native_password'
    )
    return connection



def get_emails():

    query1 = "SELECT * FROM `group` WHERE service = %s"
    query2 = "SELECT email_addr FROM participant WHERE groups_idgroup = %s"

    mydb = connect_mysql()
    mycursor = mydb.cursor()

    service = 'reserved-leonardo'

    mycursor.execute(query1, (service, ))
    myresult = mycursor.fetchall()
    for res in myresult:
        print("{0} - {1} - {2}".format(res[0], res[1], res[2]))

    gid = myresult[0][0]
    mycursor.execute(query2, (gid, ))
    myresult = mycursor.fetchall()
    emails_lst = []
    for res in myresult:
        emails_lst.append(res[0])
        #print("email: ", res[0])

    mycursor.close()

    return emails_lst
