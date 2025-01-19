import pandas as pd
import random

# Should run inside database folder

### TABLE, TABLEFORONE, TABLEFORFOUR

# Set a seed for reproducibility
random.seed(14)

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

# Generate 25 single tables
data, subclass_data, table_id = generate_table_data(
    table_id, 25, -1, [100, 0], {"cubicle.jpg": 100}, "One"
)
table_data.extend(data)
table_for_one_data.extend(subclass_data)

# Generate 5 quadruple tables
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

# Creating DataFrames
table_df = pd.DataFrame(table_data, columns=["TableID", "FloorNumber", "Image", "HasPlug"])
table_for_one_df = pd.DataFrame(table_for_one_data, columns=["TableID", "HasComputer"])
table_for_four_df = pd.DataFrame(table_for_four_data, columns=["TableID"])

# Saving to CSV files
table_csv_path = "tables.csv"
table_for_one_csv_path = "tables_for_one.csv"
table_for_four_csv_path = "tables_for_four.csv"

table_df.to_csv(table_csv_path, index=False)
table_for_one_df.to_csv(table_for_one_csv_path, index=False)
table_for_four_df.to_csv(table_for_four_csv_path, index=False)

table_csv_path, table_for_one_csv_path, table_for_four_csv_path



# # attribute distribution visualization

# import matplotlib.pyplot as plt

# # Define a function to visualize all distributions side by side
# def visualize_all_attributes():
#     fig, axes = plt.subplots(2, 2, figsize=(16, 12))  # Create a grid of subplots

#     # Table CSV visualizations
#     table_df["HasPlug"].value_counts(normalize=True).plot(
#         kind="bar", ax=axes[0, 0], title="HasPlug Distribution in Table", ylabel="Percentage (%)"
#     )
#     table_df["Image"].value_counts(normalize=True).plot(
#         kind="bar", ax=axes[0, 1], title="Image Distribution in Table", ylabel="Percentage (%)"
#     )
#     table_df["TableType"].value_counts(normalize=True).plot(
#         kind="bar", ax=axes[1, 0], title="TableType Distribution in Table", ylabel="Percentage (%)"
#     )

#     # TableForOne visualization
#     table_for_one_df["HasComputer"].value_counts(normalize=True).plot(
#         kind="bar", ax=axes[1, 1], title="HasComputer Distribution in TableForOne", ylabel="Percentage (%)"
#     )

#     # Set overall layout
#     plt.tight_layout()
#     plt.show()


# # Call the function to display all visualizations
# visualize_all_attributes()
