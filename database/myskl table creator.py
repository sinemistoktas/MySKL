import os
import sys
import subprocess
import pandas as pd

# Add the backend directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(current_dir, "../backend")
sys.path.append(backend_dir)

# Import the db_connection function
from db_connection import get_connection

## Global parameters (same ones are used in app.py)
# Define your database parameters
# # Get SQL connection password from user
password = input("Enter your root user's password for the SQL connection: ").strip()
# password = "*comp*306*st*"  # Replace with your MySQL root password
database_name = "MYSKL2" # Replace with your database name


def generate_txt_files(data_creator_script):
    """
    Execute Python scripts to generate TXT files.

    Parameters:
        data_creator_scripts (list): List of file paths for the data creator scripts.
    """
    
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of the current script
    script_path = os.path.join(script_dir, data_creator_script)  # Full path to the script

    print(f"Running {script_path}...")
    print()
    subprocess.run(["python", script_path], check=True)
    print("----- All TXT files have been created -----")
    print()

# def get_unique_database_name(cursor, base_name="MYSKL"):
#     """
#     Generate a unique database name by checking for existing databases.

#     Parameters:
#         cursor: MySQL cursor object.
#         base_name (str): Base name for the database.

#     Returns:
#         str: Unique database name.
#     """
#     cursor.execute("SHOW DATABASES;")
#     existing_databases = {db[0] for db in cursor.fetchall()}
    
#     # Check for uniqueness and increment name if necessary
#     unique_name = base_name
#     counter = 2
#     while unique_name in existing_databases:
#         unique_name = f"{base_name}{counter}"
#         counter += 1
#     return unique_name

def create_tables(cursor):
    """
    Create all tables in the database using the given relational model.
    """
    table_creation_queries = [
        """
        CREATE TABLE TableDetails (
            TableID CHAR(4),
            TableNum INT,
            FloorNumber INT,
            Image VARCHAR(255),
            HasPlug BOOLEAN,
            PRIMARY KEY (TableID)
        );
        """,
        """
        CREATE TABLE TablesForOne (
            TableID CHAR(4),
            HasComputer BOOLEAN,
            PRIMARY KEY (TableID),
            FOREIGN KEY (TableID) REFERENCES TableDetails(TableID)
        );
        """,
        """
        CREATE TABLE TablesForFour (
            TableID CHAR(4),
            PRIMARY KEY (TableID),
            FOREIGN KEY (TableID) REFERENCES TableDetails(TableID)
        );
        """,
        """
        CREATE TABLE Students (
            StudentID INT,
            StName VARCHAR(50),
            Major VARCHAR(50),
            Gender ENUM('Male', 'Female', 'Other'),
            StRating FLOAT,
            Level INT,
            XP INT,
            Password VARCHAR(30),
            PRIMARY KEY (StudentID)
        );
        """,
        """
        CREATE TABLE StandardStudents (
            StudentID INT,
            PRIMARY KEY (StudentID),
            FOREIGN KEY (StudentID) REFERENCES Students(StudentID)
        );
        """,
        """
        CREATE TABLE PremiumStudents (
            StudentID INT,
            Emoji VARCHAR(50),
            PRIMARY KEY (StudentID),
            FOREIGN KEY (StudentID) REFERENCES Students(StudentID)
        );
        """,
        """
        CREATE TABLE Alarms (
            senderID INT,
            AlertTime DATETIME,
            PRIMARY KEY (senderID, AlertTime),
            FOREIGN KEY (senderID) REFERENCES PremiumStudents(StudentID)
        );
        """,
        """
        CREATE TABLE Schedules (
            StudentID INT,
            Date DATE,
            TableID CHAR(4) DEFAULT NULL,
            Slot_1 INT DEFAULT 0,
            Slot_2 INT DEFAULT 0,
            Slot_3 INT DEFAULT 0,
            Slot_4 INT DEFAULT 0,
            Slot_5 INT DEFAULT 0,
            Slot_6 INT DEFAULT 0,
            Slot_7 INT DEFAULT 0,
            Slot_8 INT DEFAULT 0,
            PRIMARY KEY (StudentID, Date),
            FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
            FOREIGN KEY (TableID) REFERENCES TableDetails(TableID)
        );
        """,
        """
        CREATE TABLE Agreements (
            ratorID INT NOT NULL,
            rateeID INT NOT NULL,
            TableID CHAR(4),
            AgrRate INT DEFAULT -1,
            AgrDate DATE NOT NULL,
            PRIMARY KEY (ratorID, rateeID, TableID),
            FOREIGN KEY (ratorID) REFERENCES Students(StudentID),
            FOREIGN KEY (rateeID) REFERENCES Students(StudentID),
            FOREIGN KEY (TableID) REFERENCES TableDetails(TableID)
        );
        """
    ]

    for query in table_creation_queries:
        cursor.execute(query)
    
    print("----- All SQL tables are created. -----")
    print()

def number_of_rows_inserted(cursor, table_name):

    check_query = f"SELECT COUNT(*) AS row_count FROM {table_name};"
    # check_query = f"SELECT * FROM {table_name};" 

    cursor.execute(check_query)
    results = cursor.fetchall()  # Fetch all rows
    print()
    for row in results:
        print(row)  # Print each row

def populate_tables(cursor, txt_files):
    """
    Populate tables with data from the TXT files.

    Parameters:
        cursor: MySQL cursor object.
        txt_files (dict): Dictionary mapping table names to TXT file paths.
    """
    ## Add 0000 as tableID for handling NaN values in Schedules
    # Define the SQL query
    dummy_query = """
    INSERT INTO TableDetails (TableID, TableNum, FloorNumber, Image, HasPlug) 
    VALUES (%s, %s, %s, %s, %s);
    """
    values = ('0000', 0, 0, 'dummy', False) # Define the values to insert
    cursor.execute(dummy_query, values) # Execute the query with values

    # Directory where the database is located
    current_dir = os.path.dirname(os.path.abspath(__file__))

    for table_name, txt_path in txt_files.items():
        txt_path = os.path.join(current_dir, txt_path) 

        # Skip the first row as it contains column names
        insert_query = f"LOAD DATA LOCAL INFILE '{txt_path}' INTO TABLE {table_name} FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n' IGNORE 1 ROWS;"
        cursor.execute(insert_query)

        print(f"Data inserted into table {table_name}.")
        number_of_rows_inserted(cursor, table_name)

def initialize_database_and_import_txts(txt_files, password, db_name):
    """
    Create a new unique database using db_connection, create tables, and populate them.

    Parameters:
        txt_files (dict): Dictionary mapping table names to TXT file paths.
        base_db_name (str): Base name for the database.
    """
    try:
        connection = get_connection(password, db_name)
        cursor = connection.cursor()
        print("----- Connected to SQL -----")

        # Get a unique database name
        #db_name = get_unique_database_name(cursor, base_name=base_db_name)

        # Drop database if it already exists
        cursor.execute(f"DROP DATABASE IF EXISTS {db_name};")
        
        # Create the database
        cursor.execute(f"CREATE DATABASE {db_name};")
        cursor.execute(f"USE {db_name};")
        
        print(f"Database {db_name} is created and in use.")
        
        # Create tables and populate them
        create_tables(cursor)
        populate_tables(cursor, txt_files)
        
        print("All tables populated successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# Relation names and paths to the TXT files
table_names_txt_files = {
    "TableDetails": "tables.txt", # changed name from tables to table_details because SQL didnt allow the name tables
    "TablesForOne": "tables_for_one.txt",
    "TablesForFour": "tables_for_four.txt",
    "Students": "students.txt",
    "StandardStudents": "standard_students.txt",
    "PremiumStudents": "premium_students.txt",
    "Alarms": "alarms.txt",
    "Agreements": "agreements.txt",
    "Schedules": "schedules.txt",
}

# Main execution
if __name__ == "__main__":
    print()
    # Generate TXT files
    generate_txt_files("txt data creator.py")
    
    # Initialize database and import TXTs
    initialize_database_and_import_txts(table_names_txt_files, password, database_name)

