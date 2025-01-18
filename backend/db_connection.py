import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Comp306Eren", 
        auth_plugin='mysql_native_password',
        database='your_database_name'
    )
    return connection
