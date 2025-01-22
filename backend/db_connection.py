import mysql.connector

def get_connection(password, database_name, new=False):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd=password,
            allow_local_infile= True,
            autocommit = True # Set autocommit to True    
        )
        if new:
            cursor = connection.cursor()
            cursor.execute(f"DROP DATABASE IF EXISTS {database_name};")  # Drop database if it already exists
            cursor.execute(f"CREATE DATABASE {database_name};") # Create the database
        else:
            connection.database = database_name  # This sets the database for the connection


        print()
        return connection

    except Exception as e:
        print(f"General Error: {e}")