import pandas as pd
import random
from datetime import datetime, timedelta

# Set random seed for reproducibility
random.seed(14)

# Global Parameters
num_tables = 100

num_students = 500

num_alarms = 40
date_range_days = 30 # Past 30 days
min_hours = 10  # Start of slot 1 -> 10.00 
max_hours = 18  # Start of slot 8 -> 18.00 
fixed_start_date = datetime(2025, 2, 1)  # Fixed reference date
slots_per_day = 8
num_agreements = 30
num_additional_schedules = 40 # Number of additional schedules to generate


# Common Functions
def generate_skewed_level():
    """Generate a skewed level."""
    category = random.choices(['low', 'medium', 'high'], weights=[50, 40, 10], k=1)[0] # Lower, Medium, Higher levels
    if category == 'low':
        return random.randint(1, 10)
    elif category == 'medium':
        return random.randint(11, 30)
    else:
        return random.randint(31, 50)

def generate_random_date():
    """Generate a random date within a specified range."""
    random_date = fixed_start_date - timedelta(days=random.randint(0, date_range_days))
    return random_date.date()

def generate_random_time(startTime=0, endTime=23, start_of_hour=False):
    """
    Generate a random time within a specified range.
        * start_of_hour (bool): If True, minute is always 0. 
                                If False, minute is a random value between 0-59.
    """
    random_hour = random.randint(startTime, endTime)
    random_minute = 0 if start_of_hour else random.randint(0, 59)
    return datetime.min.time().replace(hour=random_hour, minute=random_minute, second=0, microsecond=0)

def generate_random_datetime(startTime=0, endTime=23, start_of_hour=False):
    """
    Generate a random datetime within range by combine random date and time into a datetime object.
        * start_of_hour (bool): Controls whether time should be at the start of the hour.
    """
    random_date = generate_random_date()
    random_time = generate_random_time(startTime=startTime, endTime=endTime, start_of_hour=start_of_hour)
    return datetime.combine(random_date, random_time)
    

# Dataset Generators
def create_tables():
    """Generate table data."""
    # Helper function to generate table data
    def generate_table_data(table_id_start, count, floor_number, has_plug_distribution, image_distribution, table_type):
        data = []
        subclass_data = []
        table_id = table_id_start
        for _ in range(count):
            has_plug = random.choices([True, False], weights=has_plug_distribution, k=1)[0]
            image = random.choices(list(image_distribution.keys()), weights=list(image_distribution.values()), k=1)[0]
            data.append([table_id, floor_number, image, has_plug])

            # Subclass-specific data
            if table_type == "One":
                subclass_data.append([table_id, random.choices([True, False], weights=[20, 80], k=1)[0]])  # Random HasComputer
            elif table_type == "Four":
                subclass_data.append([table_id])  # No additional fields for TableForFour

            table_id += 1
        return data, subclass_data, table_id

    # Generating data for tables
    table_data = []
    table_for_one_data = []
    table_for_four_data = []

    table_id = 1

    # Floor -1 (25 single tables, 5 four tables)
    data, subclass_data, table_id = generate_table_data(
        table_id, 25, -1, [100, 0], {"cubicle.jpg": 100}, "One"
    )
    table_data.extend(data)
    table_for_one_data.extend(subclass_data)

    data, subclass_data, table_id = generate_table_data(
        table_id, 5, -1, [0, 100], {"common-table.jpg": 100}, "Four"
    )
    table_data.extend(data)
    table_for_four_data.extend(subclass_data)

    # Floor 0 (20 single tables, 10 quadruple tables)
    data, subclass_data, table_id = generate_table_data(
        table_id, 20, 0, [50, 50], {"cubicle.jpg": 70, "common-table.jpg": 30}, "One"
    )
    table_data.extend(data)
    table_for_one_data.extend(subclass_data)

    data, subclass_data, table_id = generate_table_data(
        table_id, 10, 0, [0, 100], {"square.jpg": 60, "rectangle.jpg": 40}, "Four"
    )
    table_data.extend(data)
    table_for_four_data.extend(subclass_data)

    # Floor 1 (40 single tables, 10 quadruple tables)
    data, subclass_data, table_id = generate_table_data(
        table_id, 40, 1, [75, 25], {"cubicle.jpg": 80, "common-table.jpg": 20}, "One"
    )
    table_data.extend(data)
    table_for_one_data.extend(subclass_data)

    data, subclass_data, table_id = generate_table_data(
        table_id, 10, 1, [100, 0], {"square.jpg": 90, "rectangle.jpg": 10}, "Four"
    )
    table_data.extend(data)
    table_for_four_data.extend(subclass_data)

    # Floor 2 (30 single tables, 20 quadruple tables)
    data, subclass_data, table_id = generate_table_data(
        table_id, 30, 2, [33, 67], {"with-computer.jpg": 33, "common-table.jpg": 44, "cubicle.jpg": 22}, "One"
    )
    table_data.extend(data)
    table_for_one_data.extend(subclass_data)

    data, subclass_data, table_id = generate_table_data(
        table_id, 20, 2, [50, 50], {"rectangle.jpg": 70, "square.jpg": 30}, "Four"
    )
    table_data.extend(data)
    table_for_four_data.extend(subclass_data)

    # Create DataFrames
    tables_df = pd.DataFrame(table_data, columns=["TableID", "FloorNumber", "Image", "HasPlug"])
    tables_for_one_df = pd.DataFrame(table_for_one_data, columns=["TableID", "HasComputer"])
    tables_for_four_df = pd.DataFrame(table_for_four_data, columns=["TableID"])

    print("Tables data created.")
    return tables_df, tables_for_one_df, tables_for_four_df  

def create_students():
    """Generate student data."""

    turkish_first_names = {
    'Male': ["Emre", "Ahmet", "Mehmet", "Ali", "Mustafa", "Hüseyin", "Hasan", "Yusuf", "İbrahim", "Osman", "Cem", "Murat", "Kaan", "Berk", "Ege", "Oğuz", "Turan", "Uğur", "Selim", "Furkan", "Atalay", "Eren"],
    'Female': ["Beren", "Ayşe", "Fatma", "Zeynep", "Emine", "Hatice", "Elif", "Havva", "Sibel", "Büşra", "Nur", "Ece", "Merve", "Dilara", "Ceren", "Berfin", "Gül", "Yasemin", "İpek", "Selin", "Duygu", "Sinemis", "Eda"],
    'Other': ['Deniz', 'Doğa', 'Yıldız', 'Evren', 'Ozan', 'Arin', 'Utku']
    }
    turkish_last_names = ['Yılmaz', 'Kaya', 'Demir', 'Çelik', 'Şahin', 'Koç', 'Aydın', 'Erdem', 'Polat', 'Öztürk',  "Altun", "Çetin", "Güneş", "Aksoy", "Toktaş"]

    emoji_options = ['🔥', '🌊', '🗿', '🌀']

    majors = ['Bilgisayar Mühendisliği', 'Makine Mühendisliği', 'Matematik', 'Fizik', 'Biyoloji', 'İşletme', 'Medya', 'Psikoloji', 'Hukuk']

    students, standard_students, premium_students = [], [], []

    for student_id in range(1, num_students + 1):
         # Determine gender
        gender = random.choices(['Male', 'Female', 'Other'], weights=[40, 50, 10], k=1)[0] # gender distribution: Male, Female, Other
        # Assign name based on gender
        first_name = random.choice(turkish_first_names[gender])
        last_name = random.choice(turkish_last_names)
        name = f"{first_name} {last_name}"
        # Assign other attributes
        major = random.choice(majors)
        user_rating = round(random.triangular(0, 5, 4.5), 1) # Skew towards higher ratings with more weight on the upper end
        level = generate_skewed_level()
        xp = random.choice(range(0, 100, 5))  # XP in multiples of 5 within 0-99
        password = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789*-?!_.', k=8))

        # Add to students
        students.append([student_id, name, major, gender, user_rating, level, xp, password])

        # Determine student type (Standard or Premium)
        if level <= 30: # standard
            standard_students.append([student_id])
        else: # premium
            premium_students.append([student_id, random.choice(emoji_options)])

    # Create DataFrames
    students_df = pd.DataFrame(students, columns=['StudentID', 'Sname', 'Major', 'Gender', 'StRating', 'Level', 'XP', 'Password'])
    standard_students_df = pd.DataFrame(standard_students, columns=['StudentID'])
    premium_students_df = pd.DataFrame(premium_students, columns=['StudentID', 'Emoji'])

    print("Students data created.")
    return students_df, standard_students_df, premium_students_df    

def create_alarms(premium_students_df):
    """Generate alarm data."""
    premium_students_ids = premium_students_df["StudentID"].tolist() # Get PremiumStudent data

    # Generate Alarms data
    alarms = []
    for _ in range(num_alarms):
        sender_id = random.choice(premium_students_ids)  # Random PremiumStudent ID as sender
        alert_time = generate_random_datetime(startTime=min_hours, endTime=max_hours)  # Random alert time between working hours 10.00 - 18.00
        alarms.append([sender_id, alert_time])  # Add to Alarms table
    
    print("Alarms data created.")
    return pd.DataFrame(alarms, columns=["senderID", "AlertTime"])

def create_agreements_and_schedules(student_ids, table_ids):
    """Generate agreement data."""

    ratings_range = (1, 5) # agreement rating range [1, 5]

    # Generate agreements
    ids = []
    agreements = []
    schedules = []

    for _ in range(num_agreements):
        # Randomly select rator until a new one is found
        while True:
            rator_id = random.choice(student_ids)
            if rator_id not in ids:
                ids.append(rator_id)
                break  # Exit the loop when a new rator is found

        # Randomly assign a table to the rator
        rator_table_id = random.choice(table_ids) if random.random() < 0.5 else None

        # Randomly select ratee until a new one is found
        while True:
            ratee_id = random.choice(student_ids)
            if ratee_id not in ids and ratee_id != rator_id:
                ids.append(ratee_id)
                break  # Exit the loop when a new ratee is found

        # Assign a table to the ratee based on the rator's table ownership
        ratee_table_id = None if rator_table_id else random.choice(table_ids) # ratee has table if rator doesn't have one

        # Generate CreatedDate and AgrDate
        created_date = generate_random_datetime()
        agr_date = created_date + timedelta(days=random.randint(0, 5)) # AgrDate can be up to 5 days after CreatedDate
        agr_date = datetime.combine(agr_date.date(), generate_random_time(startTime=min_hours, endTime=max_hours, start_of_hour=True)) # agr times are at slot beginnings -> start of hours

        # Generate random consecutive slots for the agreement
        start_slot = random.randint(0, slots_per_day - 1)  # Random start point
        end_slot = random.randint(start_slot + 1, slots_per_day)  # Ensure end_slot is after start_slot
        agreement_slots = list(range(start_slot, end_slot))  # Generate the consecutive slots

        # Generate slot values for rator and ratee
        rator_slots = [1 if i in agreement_slots else random.randint(0, 1) for i in range(slots_per_day)]
        ratee_slots = [0 if i in agreement_slots else random.randint(0, 1) for i in range(slots_per_day)]

        # Create two agreement rows (rator and ratee perspectives)
        agr_rate_rator = random.randint(*ratings_range)
        agr_rate_ratee = random.randint(*ratings_range)
        agreements.append([rator_id, ratee_id, rator_table_id, agr_rate_rator, created_date, agr_date] + rator_slots)
        agreements.append([ratee_id, rator_id, ratee_table_id, agr_rate_ratee, created_date, agr_date] + ratee_slots)

        # Add schedules for rator and ratee
        schedules.append([rator_id, agr_date.date(), rator_table_id] + rator_slots)
        schedules.append([ratee_id, agr_date.date(), ratee_table_id] + ratee_slots)
    
    ### Generate more schedule data
    for _ in range(num_additional_schedules):
        while True:
            std_id = random.choice(student_ids) # get random student
            if std_id not in ids:
                ids.append(std_id)
                break  # Exit the loop when a new stundent is found

        date = generate_random_date() # create random date 
        table_id = random.choice(table_ids) if random.random() < 0.5 else None # has a table with 50% chance 
        slots = [random.randint(0, 1) for _ in range(slots_per_day)] # generate random slots 
        schedules.append([std_id, date, table_id] + slots)

    # Create agreements and schedules DataFrames
    agreements_df = pd.DataFrame(agreements, columns=["ratorID", "rateeID", "TableID", "AgrRate", "CreatedDate", "AgrDate"] + [f"Slot_{i}" for i in range(1, slots_per_day + 1)])
    schedules_df = pd.DataFrame(schedules, columns=["StudentID", "Date", "TableID"] + [f"Slot_{i}" for i in range(1, slots_per_day + 1)])

    print("Agreements data created.")
    print("Schedules data created.")
    return agreements_df, schedules_df


# Execution and Saving Function
def mother():
    """Generate and save all datasets."""
    tables_df, tables_for_one_df, tables_for_four_df = create_tables()
    students_df, standard_students_df, premium_students_df = create_students()
    alarms_df = create_alarms(premium_students_df)

    student_ids = students_df["StudentID"].tolist() 
    table_ids = tables_df["TableID"].tolist() 
    agreements_df, schedules_df = create_agreements_and_schedules(student_ids, table_ids)
    
    tables_df.to_csv("tables.csv", index=False)
    tables_for_one_df.to_csv("tables_for_one.csv", index=False)
    tables_for_four_df.to_csv("tables_for_four.csv", index=False)
    students_df.to_csv("students.csv", index=False)
    standard_students_df.to_csv("standard_students.csv", index=False)
    premium_students_df.to_csv("premium_students.csv", index=False)
    alarms_df.to_csv("alarms.csv", index=False)
    agreements_df.to_csv("agreements.csv", index=False)
    schedules_df.to_csv("schedules.csv", index=False)    

    print("❤︎ ❤︎ ❤︎ All datasets created and saved as csv. ❤︎ ❤︎ ❤︎")

if __name__ == "__main__":
    mother()
