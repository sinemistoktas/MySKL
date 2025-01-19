import pandas as pd
import random
from datetime import datetime, timedelta

# Set random seed for reproducibility
random.seed(14)

# Load PremiumStudent data
premium_students_df = pd.read_csv("premium_students.csv")
premium_student_ids = premium_students_df["StudentID"].tolist()

# Parameters for alarm generation
num_alarms = 40  # Total number of alarms
time_range_start = 9  # 9:00 AM
time_range_end = 17  # 5:00 PM
date_range_days = 30  # Past 30 days
fixed_start_date = datetime(2025, 1, 1)  # Fixed reference date

# Helper function to generate a random datetime within range
def generate_random_datetime():
    random_date = fixed_start_date - timedelta(days=random.randint(0, date_range_days))
    random_hour = random.randint(time_range_start, time_range_end - 1)
    random_minute = random.randint(0, 59)
    return random_date.replace(hour=random_hour, minute=random_minute, second=0, microsecond=0)

# Generate Alarms data
alarms = []

for _ in range(num_alarms):
    sender_id = random.choice(premium_student_ids)  # Random PremiumStudent ID as sender
    alert_time = generate_random_datetime()  # Random alert time
    alarms.append([sender_id, alert_time])  # Add to Alarms table

# Create DataFrame
alarms_df = pd.DataFrame(alarms, columns=["senderID", "AlertTime"])

# Save to CSV file
alarms_csv_path = "alarms.csv"
alarms_df.to_csv(alarms_csv_path, index=False)

print(f"Alarms data saved to {alarms_csv_path}")
