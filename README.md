# MySKL
A library desk-sharing system using Python, MySQL and Flask.

## Team Members:
Muhammet Eren Özoğul, Eda Engin, Sinemis Toktaş, Atalay Görgün

## Project Idea:
Our project MySKL aims for people to choose their time intervals throughout the day to study in the library and match those people with others with the opposite schedule so that they can both study on that day by using only one place. After the day finishes, both people rank their experience so that when choosing a person to share a desk, people can know how liable they are (e.g., if someone agrees with someone but the other person leaves the table without their pair, they can be ranked low).


## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/sinemistoktas/MySKL.git
   ```

2. **Create a Virtual Environment & Install Dependencies**
   Run the below code in terminal in the same directory as myskl.yml to create an environment with required dependencies.
   ```bash
   conda env create --file myskl.yml
   ```

3. **Enable Local File Loading in mysql**
   Run the following command in your MySQL client:
   ```mysql
   SET GLOBAL local_infile = 1;
   ```

4. **Data Creation**
   Run 'myskl table creator.py' in the database folder to create csv files and their corresponding SQL tables in your database.