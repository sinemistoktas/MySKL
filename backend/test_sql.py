import mysql.connector

try: 



    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd= "Comp306Eren", # "*comp*306*st*",
        auth_plugin='mysql_native_password',
        database="MySKL1"
    )
    cursor = connection.cursor()

    # Test query
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()
    print("Tables in the database:", tables)

    # Test insertion
    cursor.execute("""
    INSERT INTO Student (StudentID, S_name, Major, Sex, userRating, Level, xp, Password)
    VALUES (1, 'TestUser', 'CS', 'Male', NULL, NULL, NULL, 'testpass')
    """)
    connection.commit()
    print("Test data inserted successfully!")

    cursor.close()
    connection.close()
except mysql.connector.Error as err:
    print(f"MySQL Error: {err}")
except Exception as e:
    print(f"General Error: {e}")
