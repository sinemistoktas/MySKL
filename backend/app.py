from flask import Flask, send_from_directory, jsonify, request
import mysql.connector
from flask_cors import CORS

# Database connection function
from db_connection import get_connection

app = Flask(__name__, static_folder='../client/build')
CORS(app)

## Global parameters
# Define your database parameters
# # Get SQL connection password from user
#password = input("Enter your root user's password for the SQL connection: ").strip()
password = "*comp*306*st*"  # Replace with your MySQL root password
database_name = "MYSKL2" # Replace with your database name

# Create a single connection at the start
connection = get_connection(password, database_name)
print("----- Connected to SQL -----")

# Serve the React app
@app.route('/', methods=['GET'])
def serve_react_app():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>', methods=['GET'])
def serve_static_files(path):
    return send_from_directory(app.static_folder, path)

@app.route('/login', methods=['POST'])
def login_student():
    try:
        data = request.json
        student_id = data.get('StudentID')
        password = data.get('Password')

        if not student_id or not password:
            return jsonify({'error': 'StudentID and Password are required!'}), 400

        # Reuse the existing connection
        cursor = connection.cursor(dictionary=True)

        # Query to check if the student exists and password matches
        query = "SELECT * FROM Students WHERE StudentID = %s AND Password = %s"
        cursor.execute(query, (student_id, password))
        result = cursor.fetchone()

        cursor.close()
        # connection.close()

        if result:
            return jsonify({'message': 'Login successful!', 'student': result}), 200
        else:
            return jsonify({'error': 'Invalid StudentID or Password'}), 401

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return jsonify({'error': str(err)}), 500
    except Exception as e:
        print(f"General Error: {e}")
        return jsonify({'error': str(e)}), 400

# API Endpoint to register a new student
@app.route('/register', methods=['POST'])
def register_student():
    try:
        # Get student data from the request
        data = request.json
        student_id = data.get('StudentID')
        name = data.get('Stname')
        major = data.get('Major')
        sex = data.get('Gender')
        password = data.get('Password')
        is_premium = data.get('isPremium', False)  # Indicates if the student is premium
        emoji = data.get('Emoji', '')  # Emoji for premium students (optional)

        # Validate required fields
        if not all([student_id, name, major, sex, password]):
            return jsonify({'error': 'All fields are required!'}), 400

        # # Connect to MySQL
        # connection = get_connection()

        # Reuse the existing connection
        cursor = connection.cursor()

        # Insert into the `Student` table
        student_query = """
        INSERT INTO Students (StudentID, Stname, Major, Gender, stRating, Level, XP, Password)
        VALUES (%s, %s, %s, %s, 0.0, 1, 0, %s)
        """
        cursor.execute(student_query, (student_id, name, major, sex, password))

        # Insert into the appropriate table based on `is_premium`
        if is_premium:
            premium_query = """
            INSERT INTO PremiumStudents (StudentID, Emoji)
            VALUES (%s, %s)
            """
            cursor.execute(premium_query, (student_id, emoji))
            student_type = "PremiumStudent"
        else:
            standard_query = """
            INSERT INTO StandardStudents (StudentID)
            VALUES (%s)
            """
            cursor.execute(standard_query, (student_id,))
            student_type = "StandardStudent"

        # # Commit the transaction, autocommit is open so I uncommented this
        # connection.commit()

        # Close the connection
        cursor.close()
        # connection.close()

        # Respond with success
        return jsonify({'message': f'{student_type} registered successfully!'}), 201

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")  # Log the MySQL error
        return jsonify({'error': str(err)}), 500
    except Exception as e:
        print(f"General Error: {e}")  # Log any general errors
        return jsonify({'error': str(e)}), 400

@app.route('/schedule/<student_id>', methods=['GET'])
def get_schedule(student_id):
    try:
        # connection = get_connection()
        # Reuse the existing connection
        cursor = connection.cursor(dictionary=True)
        
        # Check if student has a schedule
        query = """
        SELECT *
        FROM Schedules
        WHERE StudentID = %s
        """
        cursor.execute(query, (student_id,))
        result = cursor.fetchone()
        
        cursor.close()
        # connection.close()
        
        if result:
            return jsonify({'hasSchedule': True, 'schedule': result}), 200
        else:
            return jsonify({'hasSchedule': False}), 200
            
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/schedule', methods=['POST'])
def create_schedule():
    try:
        data = request.json
        student_id = data.get('StudentID')
        date = data.get('Date')
        slots = data.get('Slots')  # Array of slot values
        
        # Create ScheduleID by combining date and student_id
        # Remove hyphens from date and concatenate with student_id
        date_str = date.replace('-', '')
        schedule_id = f"{date_str}{student_id}"  # Keep as string, don't convert to int
        
        # connection = get_connection()
        # Reuse the existing connection
        cursor = connection.cursor()

        # First check if a schedule already exists for this student and date
        check_query = """
        SELECT ScheduleID FROM HasSchedule 
        WHERE StudentID = %s AND Date = %s
        """
        cursor.execute(check_query, (student_id, date))
        existing_schedule = cursor.fetchone()

        if existing_schedule:
            # If exists, update the slots
            update_query = """
            UPDATE SlotStatus 
            SET Slot1=%s, Slot2=%s, Slot3=%s, Slot4=%s, Slot5=%s, Slot6=%s, Slot7=%s, Slot8=%s
            WHERE ScheduleID = %s AND SlotID = 1
            """
            cursor.execute(update_query, (*slots, existing_schedule[0]))
            message = 'Schedule updated successfully'
        else:
            # If not exists, create new schedule with the generated schedule_id
            schedule_query = """
            INSERT INTO HasSchedule (ScheduleID, StudentID, Date)
            VALUES (%s, %s, %s)
            """
            cursor.execute(schedule_query, (schedule_id, student_id, date))
            
            # Insert into SlotStatus
            slot_query = """
            INSERT INTO SlotStatus (ScheduleID, SlotID, Slot1, Slot2, Slot3, Slot4, Slot5, Slot6, Slot7, Slot8)
            VALUES (%s, 1, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(slot_query, (schedule_id, *slots))
            message = 'Schedule created successfully'
        
        # connection.commit()
        cursor.close()
        # connection.close()
        
        return jsonify({'message': message, 'scheduleId': schedule_id}), 201
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/schedule/<schedule_id>', methods=['DELETE'])
def delete_schedule(schedule_id):
    try:
        # connection = get_connection()
        # Reuse the existing connection
        cursor = connection.cursor()
        
        # Delete from SlotStatus first (child table)
        delete_slots_query = "DELETE FROM SlotStatus WHERE ScheduleID = %s"
        cursor.execute(delete_slots_query, (schedule_id,))
        
        # Then delete from HasSchedule (parent table)
        delete_schedule_query = "DELETE FROM HasSchedule WHERE ScheduleID = %s"
        cursor.execute(delete_schedule_query, (schedule_id,))
        
        # connection.commit()
        cursor.close()
        # connection.close()
        
        return jsonify({'message': 'Schedule deleted successfully'}), 200
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500
    
@app.route('/alerts', methods=['POST'])
def create_alert(): # create alert
    try:
        data = request.json
        sender_id = data.get('senderID')
        alert_time = data.get('AlertTime')

        if not sender_id or not alert_time:
            return jsonify({'error': 'SenderID and AlertTime are required!'}), 400

        # Verify the sender is a PremiumStudent
        cursor = connection.cursor()
        premium_check_query = "SELECT StudentID FROM PremiumStudents WHERE StudentID = %s"
        cursor.execute(premium_check_query, (sender_id,))
        is_premium = cursor.fetchone()

        if not is_premium:
            return jsonify({'error': 'Only PremiumStudents can send alerts.'}), 403

        # Insert the alert into the Alarms table
        insert_query = "INSERT INTO Alarms (senderID, AlertTime) VALUES (%s, %s)"
        cursor.execute(insert_query, (sender_id, alert_time))

        cursor.close()
        return jsonify({'message': 'Alert created successfully!'}), 201

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return jsonify({'error': str(err)}), 500
    except Exception as e:
        print(f"General Error: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/alerts', methods=['GET']) 
def get_alerts(): # fetch alerts
    try: 
        student_id = request.args.get('studentID')

        if not student_id:
            return jsonify({'error': 'StudentID is required to fetch alerts!'}), 400

        # Verify the student is a PremiumStudent
        cursor = connection.cursor(dictionary=True)
        premium_check_query = "SELECT StudentID FROM PremiumStudents WHERE StudentID = %s"
        cursor.execute(premium_check_query, (student_id,))
        is_premium = cursor.fetchone()

        if not is_premium:
            return jsonify({'error': 'Only PremiumStudents can view alerts.'}), 403

        # Fetch alerts
        fetch_query = "SELECT * FROM Alarms ORDER BY AlertTime DESC"
        cursor.execute(fetch_query)
        alerts = cursor.fetchall()

        cursor.close()
        return jsonify({'alerts': alerts}), 200

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return jsonify({'error': str(err)}), 500
    except Exception as e:
        print(f"General Error: {e}")
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
