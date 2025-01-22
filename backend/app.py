from flask import Flask, send_from_directory, jsonify, request
import mysql.connector
from flask_cors import CORS
from datetime import datetime
from db_connection import get_connection

app = Flask(__name__, static_folder='../client/build')
CORS(app)

# Global parameters
password = "Comp306Eren"  # Replace with your MySQL root password
database_name = "MySKL1"  # Replace with your database name

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

        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM Students WHERE StudentID = %s AND Password = %s"
        cursor.execute(query, (student_id, password))
        result = cursor.fetchone()
        cursor.close()

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

@app.route('/register', methods=['POST'])
def register_student():
    try:
        data = request.json
        student_id = data.get('StudentID')
        name = data.get('Stname')
        major = data.get('Major')
        sex = data.get('Gender')
        password = data.get('Password')
        is_premium = data.get('isPremium', False)
        emoji = data.get('Emoji', '')

        if not all([student_id, name, major, sex, password]):
            return jsonify({'error': 'All fields are required!'}), 400

        cursor = connection.cursor()
        student_query = """
        INSERT INTO Students (StudentID, Stname, Major, Gender, stRating, Level, XP, Password)
        VALUES (%s, %s, %s, %s, 0.0, 1, 0, %s)
        """
        cursor.execute(student_query, (student_id, name, major, sex, password))

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

        connection.commit()
        cursor.close()

        return jsonify({'message': f'{student_type} registered successfully!'}), 201

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return jsonify({'error': str(err)}), 500
    except Exception as e:
        print(f"General Error: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/schedule/<student_id>', methods=['GET'])
def get_schedule(student_id):
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT Date, Slot_1, Slot_2, Slot_3, Slot_4, Slot_5, Slot_6, Slot_7, Slot_8
        FROM Schedules
        WHERE StudentID = %s AND Date = CURDATE()
        """
        cursor.execute(query, (student_id,))
        schedule = cursor.fetchone()
        cursor.close()

        if schedule:
            return jsonify({'hasSchedule': True, 'schedule': schedule}), 200
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
        slots = data.get('Slots')

        cursor = connection.cursor()
        query = """
        INSERT INTO Schedules (StudentID, Date, Slot_1, Slot_2, Slot_3, Slot_4, Slot_5, Slot_6, Slot_7, Slot_8)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        Slot_1 = VALUES(Slot_1), Slot_2 = VALUES(Slot_2), Slot_3 = VALUES(Slot_3),
        Slot_4 = VALUES(Slot_4), Slot_5 = VALUES(Slot_5), Slot_6 = VALUES(Slot_6),
        Slot_7 = VALUES(Slot_7), Slot_8 = VALUES(Slot_8)
        """
        cursor.execute(query, (student_id, date, *slots))
        connection.commit()
        cursor.close()

        return jsonify({'message': 'Schedule created/updated successfully'}), 201

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500
    

@app.route('/schedule/<int:student_id>', methods=['DELETE'])
def delete_schedule(student_id):
    try:
        data = request.json
        date = data.get('Date')

        if not date:
            return jsonify({'error': 'Date is required to delete a schedule'}), 400

        cursor = connection.cursor()

        # Delete the schedule for the given student ID and date
        delete_query = """
        DELETE FROM Schedules 
        WHERE StudentID = %s AND Date = %s
        """
        cursor.execute(delete_query, (student_id, date))
        connection.commit()
        cursor.close()

        if cursor.rowcount == 0:
            return jsonify({'error': 'No schedule found to delete'}), 404

        return jsonify({'message': 'Schedule deleted successfully'}), 200

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return jsonify({'error': str(err)}), 500
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/today-schedules', methods=['GET'])
def get_today_schedules():
    try:
        today = datetime.now().date()

        # Query to fetch schedules for today with table image paths
        query = """
        SELECT Schedules.Date, Schedules.Slot_1, Schedules.Slot_2, Schedules.Slot_3,
               Schedules.Slot_4, Schedules.Slot_5, Schedules.Slot_6, Schedules.Slot_7, Schedules.Slot_8,
               Students.StName, TableDetails.Image AS TableImage
        FROM Schedules
        INNER JOIN Students ON Schedules.StudentID = Students.StudentID
        LEFT JOIN TableDetails ON Schedules.TableID = TableDetails.TableID
        WHERE Schedules.Date = %s
        """
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, (today,))
        schedules = cursor.fetchall()
        cursor.close()

        return jsonify({'schedules': schedules}), 200

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return jsonify({'error': str(err)}), 500
    except Exception as e:
        print(f"General Error: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/table-details/<table_id>', methods=['GET'])
def get_table_details(table_id):
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT Image FROM TableDetails WHERE TableID = %s"
        cursor.execute(query, (table_id,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            return jsonify({result['Image']}), 200
        else:
            return jsonify({'error': 'Table not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/premium-emoji/<int:student_id>', methods=['GET'])
def get_premium_emoji(student_id):
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT Emoji FROM PremiumStudents WHERE StudentID = %s"
        cursor.execute(query, (student_id,))
        result = cursor.fetchone()
        cursor.close()

        if result and result['Emoji']:
            return jsonify({'emoji': result['Emoji']}), 200
        else:
            return jsonify({'error': 'No emoji found for this user'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/create-agreement', methods=['POST'])
def create_agreement():
    try:
        data = request.json
        rator_id = data.get('ratorID')
        ratee_id = data.get('rateeID','1')
        table_id = data.get('TableID', '0000')  # Default to '0000' if not provided
        agr_date = data.get('AgrDate')

        if not all([rator_id, ratee_id, table_id, agr_date]):
            return jsonify({'error': 'All fields are required!'}), 400

        # Insert into Agreements table
        query = """
        INSERT INTO Agreements (ratorID, rateeID, TableID, AgrDate)
        VALUES (%s, %s, %s, %s)
        """
        cursor = connection.cursor()
        cursor.execute(query, (rator_id, ratee_id, table_id, agr_date))
        connection.commit()
        cursor.close()

        return jsonify({'message': 'Agreement created successfully!'}), 201

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return jsonify({'error': str(err)}), 500
    except Exception as e:
        print(f"General Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
