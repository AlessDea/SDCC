import mysql.connector

def connect_to_db():
    mydb = mysql.connector.connect(
        host="localhost",
        user="yourusername",
        password="yourpassword"
        database = "mydatabase"
    )
