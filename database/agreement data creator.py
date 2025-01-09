import pandas as pd
import random
from datetime import datetime, timedelta

# Set random seed for reproducibility
random.seed(14)

# Parameters for agreement generation
num_agreements = 100  # Total number of agreements
ratings_range = (1, 5)  # Ratings range
date_range_days = 30  # Same as alarms
fixed_start_date = datetime(2025, 1, 1)  # Fixed reference date for consistency

# Reload required data
students_df = pd.read_csv("students.csv")
table_df = pd.read_csv("table.csv")

# Helper function to generate random datetime within range
def generate_random_datetime():
    random_date = fixed_start_date - timedelta(days=random.randint(0, date_range_days))
    random_hour = random.randint(9, 17 - 1)  # 9:00 AM to 4:59 PM
    random_minute = random.randint(0, 59)
    return random_date.replace(hour=random_hour, minute=random_minute, second=0, microsecond=0)

# Generate agreements
agreements = []
student_ids = students_df["StudentID"].tolist()
table_ids = table_df["TableID"].tolist()

for _ in range(num_agreements):
    rator_id = random.choice(student_ids)
    ratee_id = random.choice([id for id in student_ids if id != rator_id])  # Avoid self-agreement
    table_id = random.choice(table_ids)
    agr_date = generate_random_datetime()  # Agreement creation time
    start_time = agr_date + timedelta(hours=random.randint(0, 3))  # Start time 0-3 hours after creation
    end_time = start_time + timedelta(hours=random.randint(1, 2))  # End time 1-2 hours after start
    agr_rate = round(random.uniform(*ratings_range), 1)  # Rating between 1 and 5
    
    agreements.append([rator_id, ratee_id, table_id, agr_date, start_time, end_time, agr_rate])

# Create DataFrame and save to CSV
agreements_df = pd.DataFrame(agreements, columns=[
    "ratorID", "rateeID", "TableID", "AgrDate", "startTime", "endTime", "AgrRate"
])
agreements_csv_path = "agreements.csv"
agreements_df.to_csv(agreements_csv_path, index=False)

agreements_csv_path
