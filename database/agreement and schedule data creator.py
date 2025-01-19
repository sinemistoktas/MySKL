import pandas as pd
import random
from datetime import datetime, timedelta

# Set random seed for reproducibility
random.seed(14)

# Global parameters
num_agreements = 30
ratings_range = (1, 5)
date_range_days = 30
fixed_start_date = datetime(2025, 1, 1)  # Fixed reference date
slots_per_day = 8
min_hours = 10  # Start of slot 1 -> 10.00 
max_hours = 18  # Start of slot 8 -> 18.00 
num_additional_schedules = 40  # Number of additional schedules to generate

# Load Student and Table data
students_df = pd.read_csv("students.csv")  # Assuming this contains a column "StudentID"
tables_df = pd.read_csv("tables.csv")  # Assuming this contains a column "TableID"

student_ids = students_df["StudentID"].tolist()
table_ids = tables_df["TableID"].tolist()

# Helper function to generate a random CreatedDate
def generate_random_created_date():
    random_days = random.randint(-date_range_days, 0)
    random_time = timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))
    return datetime.now() + timedelta(days=random_days) + random_time

# Helper function to generate a random AgrDate
def generate_random_agr_date(created_date):
    random_days = random.randint(0, 5)  # AgrDate can be up to 5 days after CreatedDate
    random_hour = random.randint(min_hours, max_hours)
    agr_date = created_date + timedelta(days=random_days)
    return agr_date.replace(hour=random_hour, minute=0, second=0, microsecond=0)

# Generate agreements
agreements = []
schedules = []
for _ in range(num_agreements):
    # Randomly select rator and ratee
    rator_id = random.choice(student_ids)
    rator_table_id = random.choice(table_ids) if random.random() < 0.5 else None

    # Select a random ratee with opposite table ownership
    ratee_candidates = [
        student_id for student_id in student_ids
        if student_id != rator_id
    ]
    if not ratee_candidates:
        continue

    ratee_id = random.choice(ratee_candidates)
    ratee_table_id = None if rator_table_id else random.choice(table_ids)

    # Generate CreatedDate and AgrDate
    created_date = generate_random_created_date()
    agr_date = generate_random_agr_date(created_date)

    # Create random slots for the agreement
    agreement_slots = random.sample(range(slots_per_day), random.randint(1, slots_per_day))  # Random subset of slots

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


# Create additional random schedules
for _ in range(num_additional_schedules):
    student_id = random.choice(student_ids)
    random_date = datetime(2025, 1, 1) - timedelta(days=random.randint(0, date_range_days))
    slots = [random.randint(0, 1) for _ in range(slots_per_day)] # generate random slots
    table_id = random.choice(table_ids) if random.random() < 0.5 else None
    schedules.append([student_id, random_date.date(), table_id] + slots)

# Create agreements and schedules DataFrames
agreement_columns = [
    "ratorID", "rateeID", "TableID", "AgrRate", "CreatedDate", "AgrDate",
    "Slot_1", "Slot_2", "Slot_3", "Slot_4", "Slot_5", "Slot_6", "Slot_7", "Slot_8"
]
agreements_df = pd.DataFrame(agreements, columns=agreement_columns)

schedule_columns = ["StudentID", "Date", "TableID"] + [f"Slot_{i}" for i in range(1, slots_per_day + 1)]
schedules_df = pd.DataFrame(schedules, columns=schedule_columns)

# Save to CSV
agreements_csv_path = "agreements.csv"
schedules_csv_path = "schedules.csv"

agreements_df.to_csv(agreements_csv_path, index=False)
schedules_df.to_csv(schedules_csv_path, index=False)

print(f"Agreements data saved to {agreements_csv_path}")
print(f"Schedules data saved to {schedules_csv_path}")
