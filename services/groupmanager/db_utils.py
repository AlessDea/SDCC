import mysql
import mysql.connector

def connect_mysql():
    try:
        connection = mysql.connector.connect(
            host="group-db-mysql-primary.default.svc.cluster.local",
            user="root",
            password="root",
            database="groupdb",
            port="3306"
        )
        return connection
    except:
        return False



def get_emails(group_name, service):

    query = "SELECT email_addr FROM gruppi WHERE group_name = %s"
    val = (group_name, service)

    mydb = connect_mysql()
    mycursor = None

    if mydb != False:
        try:
            mycursor = mydb.cursor()
            mycursor.execute(query,val)
            myresult = mycursor.fetchall()
            if mycursor.rowcount > 0:
                emails_lst = []
                for res in myresult:
                    emails_lst.append(res[0])
                return emails_lst
            return False
        except:
            return False
        finally:
            if mycursor != None:
                mycursor.close()
    else:
        return False



def get_info(group_name):

    query = "SELECT * FROM gruppi WHERE group_name = %s"
    val = (group_name)

    mydb = connect_mysql()
    mycursor = None

    if mydb != False:
        try:
            mycursor = mydb.cursor()
            mycursor.execute(query, val)
            myresult = mycursor.fetchall()
            if mycursor.rowcount > 0:
                return myresult
            return False
        except:
            return False
        finally:
            if mycursor != None:
                mycursor.close()
    else:
        return False


def create_group(group_name, username, email, service):

    query = "INSERT INTO gruppi VALUES (%s,%s,%s,%s)"
    val = (group_name, username, email, service)

    mydb = connect_mysql()
    mycursor = None
    if mydb != False:
        try:
            mydb = connect_mysql()
            mycursor = mydb.cursor()
            mycursor.execute(query,val)
            mydb.commit()
            if mycursor.rowcount > 0:
                return True
            return False
        except:
            return False
        finally:
            if mycursor != None:
                mycursor.close()
    else:
        return False
