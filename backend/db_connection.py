import mysql.connector

def get_connection(password, database_name):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd=password,
            allow_local_infile= True,
        )

        if database_name:
            connection.database = database_name  # This sets the database for the connection

        # Set autocommit to True    
        connection.autocommit = True

        print()
        return connection

    except Exception as e:
        print(f"General Error: {e}")