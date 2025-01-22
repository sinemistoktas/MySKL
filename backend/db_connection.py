import mysql.connector

def get_connection(database_name=None):
    print("----- Creating SQL connection -----")
    print("Please select your user by entering the corresponding number:")
    print("1- Eren \n2- Sinemis \n3- Eda \n4- Atalay \n5- Other/New user")
    user = input("Enter your choice: ").strip()

    # Assign password based on user choice
    if user == "1":
        password = "Comp306Eren"
    elif user == "2":
        password = "*comp*306*st*"
    elif user == "3":
        password = None
        print("No password assigned. Please add your password to db_connection.py file in backend folder")
    elif user == "4":
        password = None
        print("No password assigned. Please add your password to db_connection.py file in backend folder")
    elif user == "5":
        password = input("Enter your password: ").strip()
    else:
        password = None
        print("Invalid choice! Unknown user. Please add your user info to db_connection.py file in backend folder")

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd=password, 
            auth_plugin='mysql_native_password',
            allow_local_infile= True,
        )

        if database_name:
            connection.database = database_name  # This sets the database for the connection

        # Set autocommit to True    
        connection.autocommit = True

        print("----- Connected to SQL -----")
        print()
        return connection

    except Exception as e:
        print(f"General Error: {e}")