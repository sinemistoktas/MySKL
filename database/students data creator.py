import pandas as pd
import random

# Set random seed for reproducibility
random.seed(14)

# Parameters
total_students = 500
gender_distribution = [40, 50, 10]  # Male, Female, Other
rating_skewed_range = (3, 5)  # Most ratings between 3 and 5
level_distribution = [50, 30, 20]  # Lower, Medium, Higher levels
emoji_options = ['🔥', '🌊', '🗿', '🌀']  # Emojis for Premium Students


turkish_first_names = {
    'Male': ["Emre", "Ahmet", "Mehmet", "Ali", "Mustafa", "Hüseyin", "Hasan", "Yusuf", "İbrahim", "Osman", "Cem", "Murat", "Kaan", "Berk", "Ege", "Oğuz", "Turan", "Uğur", "Selim", "Furkan", "Atalay", "Eren"],
    'Female': ["Beren", "Ayşe", "Fatma", "Zeynep", "Emine", "Hatice", "Elif", "Havva", "Sibel", "Büşra", "Nur", "Ece", "Merve", "Dilara", "Ceren", "Berfin", "Gül", "Yasemin", "İpek", "Selin", "Duygu", "Sinemis", "Eda"],
    'Other': ['Deniz', 'Doğa', 'Yıldız', 'Evren', 'Ozan', 'Arin', 'Utku']
}
turkish_last_names = ['Yılmaz', 'Kaya', 'Demir', 'Çelik', 'Şahin', 'Koç', 'Aydın', 'Erdem', 'Polat', 'Öztürk',  "Altun", "Çetin", "Güneş", "Aksoy", "Toktaş"]

# Helper function to generate skewed ratings
def generate_skewed_rating():
    return round(random.triangular(0, 5, random.uniform(*rating_skewed_range)), 1)

# Helper function to generate skewed levels
def generate_skewed_level():
    category = random.choices(['low', 'medium', 'high'], weights=level_distribution, k=1)[0]
    if category == 'low':
        return random.randint(1, 10)
    elif category == 'medium':
        return random.randint(11, 30)
    else:
        return random.randint(31, 50)

# Generate Students
students = []
standard_students = []
premium_students = []

for student_id in range(1, total_students + 1):
    # Determine gender
    gender = random.choices(['Male', 'Female', 'Other'], weights=gender_distribution, k=1)[0]
    
    # Assign name based on gender
    first_name = random.choice(turkish_first_names[gender])
    last_name = random.choice(turkish_last_names)
    name = f"{first_name} {last_name}"

    # Assign other attributes
    major = random.choice(['Bilgisayar Mühendisliği', 'Makine Mühendisliği', 'Matematik', 'Fizik', 'Biyoloji', 'İşletme', 'Medya', 'Psikoloji', 'Hukuk'])
    rating = generate_skewed_rating()
    level = generate_skewed_level()

    # Add to students
    students.append([student_id, name, major, gender, rating, level])

    # Determine type (Standard or Premium)
    if level <= 30:
        standard_students.append([student_id])
    else:
        emoji = random.choice(emoji_options)
        premium_students.append([student_id, emoji])

# Create DataFrames
students_df = pd.DataFrame(students, columns=['StudentID', 'S_name', 'Major', 'Sex', 'Rating', 'Level'])
standard_students_df = pd.DataFrame(standard_students, columns=['StudentID'])
premium_students_df = pd.DataFrame(premium_students, columns=['StudentID', 'Emoji'])

# Save to CSV
students_csv_path = "students.csv"
standard_students_csv_path = "standard_students.csv"
premium_students_csv_path = "premium_students.csv"

students_df.to_csv(students_csv_path, index=False)
standard_students_df.to_csv(standard_students_csv_path, index=False)
premium_students_df.to_csv(premium_students_csv_path, index=False)

students_csv_path, standard_students_csv_path, premium_students_csv_path




# # # attribute distribution visualization

# import matplotlib.pyplot as plt

# fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# # Gender distribution with colors
# gender_distribution = students_df["Sex"].value_counts(normalize=True) * 100
# gender_distribution.plot(
#     kind="bar", 
#     ax=axes[0, 0], 
#     title="Gender Distribution", 
#     ylabel="Percentage (%)", 
#     color=["red", "blue", "green"]
# )

# # Rating distribution with narrower bins
# students_df["Rating"].plot(
#     kind="hist", 
#     bins=20, 
#     ax=axes[0, 1], 
#     title="Rating Distribution",
#     edgecolor="black",
#     linewidth=1.2
# )
# axes[0, 1].set_xlabel("Rating")
# axes[0, 1].set_ylabel("Frequency")

# # Level distribution with narrower bins
# students_df["Level"].plot(
#     kind="hist", 
#     bins=15, 
#     ax=axes[1, 0], 
#     title="Level Distribution",
#     edgecolor="black",
#     linewidth=1.2
# )
# axes[1, 0].set_xlabel("Level")
# axes[1, 0].set_ylabel("Frequency")

# # Standard vs Premium Students
# student_types = ["Standard", "Premium"]
# student_type_counts = [len(standard_students_df), len(premium_students_df)]
# axes[1, 1].bar(student_types, student_type_counts, color=["blue", "green"])
# axes[1, 1].set_title("Standard vs Premium Students")
# axes[1, 1].set_ylabel("Count")

# # Adjust layout for better spacing
# plt.tight_layout()
# plt.show()
