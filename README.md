# Unsircle Test

&copy; 2020 Willy Sumarno

## Installation

Here are step-by-step installation after you clone this repository. I used flask for backend and react for frontend.

### BackEnd

1. Create database ```unsircle_test_be```
2. Change your MySQL username and password in ```backend/blueprints/__init__.py``` line 35
3. Create virtual environtment, then activate it
4. Install the dependencies: ```pip install -r requirements.txt```
5. Initialize the database: ```python app.py db init```
6. Migrate the database: ```python app.py db migrate```
7. Run the app: ```python app.py```

### FrontEnd

1. Install the dependencies: ```npm install```
2. Run the app: ```npm start```
