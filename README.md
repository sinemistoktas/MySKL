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
   After creating the env, activate it:
   ```bash
   conda activate myskl
   ```

3. **Install React application requirements**
   Follow below steps for installing React requirements. You can read the README.md in the client folder for more information.
   1. Navigate to the client directory (Assuming you are in the main directory of MySKL):
      ```
      cd client
      ```
   2. Install the dependencies:
      ```
      npm install
      ```

4. **Enable Local File Loading in mysql**
   Our project uses "root" username for SQL connection. If you don’t already have a user with this username, please create one before continuing.
   
   Connect then run the following command in your MySQL client:
   ```mysql
   SET GLOBAL local_infile = 1;
   ```

5. **Data Creation**
   Run 'myskl table creator.py' in the database folder to create csv files and their corresponding SQL tables in your database.
   ```bash
   python myskl\ table\ creator.py
   ```

6. **Run the Flask Application**
   Start the Flask server. Inside backend folder's directory run:
   ```bash
   python app.py
   ```
   The Flask application link will be outputted to the terminal once the server is running. 

7. **Running the React Application** 
   To start the React application, in a new tab, run the following command in the client folder's directory:
   ```
   npm start
   ```
   This will open the website automatically.


## Usage
The Flask application will be running on `http://localhost:5000` by default. The link will be outputted to the terminal once the server is running. 
You can access the API endpoints defined in `app.py`.

## Additional Information
For more details on how to integrate with the React frontend, refer to the client-side README located in the `client` directory.