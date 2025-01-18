from flask import Flask, send_from_directory, jsonify, request
import mysql.connector
from flask_cors import CORS


app = Flask(__name__, static_folder='../client/build')
CORS(app)

# Database connection function
def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Comp306Eren",  # Replace with your MySQL password
        database="MySKL1"  # Replace with your database name
    )
    return connection

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

        # Connect to the database
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        # Query to check if the student exists and password matches
        query = "SELECT * FROM Student WHERE StudentID = %s AND Password = %s"
        cursor.execute(query, (student_id, password))
        result = cursor.fetchone()

        cursor.close()
        connection.close()

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
        name = data.get('S_name')
        major = data.get('Major')
        sex = data.get('Sex')
        password = data.get('Password')
        is_premium = data.get('isPremium', False)  # Indicates if the student is premium
        emoji = data.get('Emoji', '')  # Emoji for premium students (optional)

        # Validate required fields
        if not all([student_id, name, major, sex, password]):
            return jsonify({'error': 'All fields are required!'}), 400

        # Connect to MySQL
        connection = get_connection()
        cursor = connection.cursor()

        # Insert into the `Student` table
        student_query = """
        INSERT INTO Student (StudentID, S_name, Major, Sex, userRating, Level, xp, Password)
        VALUES (%s, %s, %s, %s, NULL, NULL, NULL, %s)
        """
        cursor.execute(student_query, (student_id, name, major, sex, password))

        # Insert into the appropriate table based on `is_premium`
        if is_premium:
            premium_query = """
            INSERT INTO PremiumStudent (StudentID, Emoji)
            VALUES (%s, %s)
            """
            cursor.execute(premium_query, (student_id, emoji))
            student_type = "PremiumStudent"
        else:
            standard_query = """
            INSERT INTO StandardStudent (StudentID)
            VALUES (%s)
            """
            cursor.execute(standard_query, (student_id,))
            student_type = "StandardStudent"

        # Commit the transaction
        connection.commit()

        # Close the connection
        cursor.close()
        connection.close()

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
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Check if student has a schedule
        query = """
        SELECT h.*, s.*
        FROM HasSchedule h
        LEFT JOIN SlotStatus s ON h.ScheduleID = s.ScheduleID
        WHERE h.StudentID = %s
        """
        cursor.execute(query, (student_id,))
        result = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
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
        
        connection = get_connection()
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
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({'message': message, 'scheduleId': schedule_id}), 201
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/schedule/<schedule_id>', methods=['DELETE'])
def delete_schedule(schedule_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        # Delete from SlotStatus first (child table)
        delete_slots_query = "DELETE FROM SlotStatus WHERE ScheduleID = %s"
        cursor.execute(delete_slots_query, (schedule_id,))
        
        # Then delete from HasSchedule (parent table)
        delete_schedule_query = "DELETE FROM HasSchedule WHERE ScheduleID = %s"
        cursor.execute(delete_schedule_query, (schedule_id,))
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({'message': 'Schedule deleted successfully'}), 200
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
