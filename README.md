# Expense-Tracker-Backend

This API runs on Python 3.6. Make sure you have Python 3.6 and pip installed.

You can access all the functionalities using it's client hosted on: 
            
            https://expensetrack-client.herokuapp.com/

# Production URL

The API is hosted on Heroku:

		https://expen-track.herokuapp.com/api/v1/expenses/
    
# URLs and Features

The API has 3 features:

1. Login/Signup using JWT authentication
2. Create, Read, Update, Delete Expenses
3. Sort/Filter expenses
4. Search Expenses by name

# Clone the Repository

Open the terminal and run the command:

		git clone https://github.com/Shwetabhk/Expense-Tracker-Backend.git

# Create a virtual environment

open your working directory in the terminal and run the following commands:

		pip install virtualenv

		python -m virtualenv env

		source env/bin/activate


# Install the requirements

Open the cloned folder in the terminal(virtual environment) and run the following commands:

		pip install -r requirements.txt


# Migrating the database

Run the following commands to make changes in the database:

		python manage.py makemigrations

		python manage.py migrate


# Run the server

		python manage.py runserver




	
