# Ferris.Finance
 
# Budget Management App

This is a simple budget management application built using Python's `tkinter` library for the GUI, `pandas` for handling data in Excel format, and `mysql.connector` for interacting with a MySQL database. The application allows users to log in or register, track their income and expenses, and export/import their transaction history to/from an Excel file.

## Prerequisites

To run the application, make sure you have the following installed:

- Python 3.x
- `tkinter`, `pandas`, and `mysql-connector-python` libraries (install using pip: `pip install tkinter pandas mysql-connector-python`)

Additionally, you need to have a running MySQL server, and it should have a user with the following credentials:

- Username: "root"
- Password: "Codegeassr1721!"

## How to Use

1. Make sure you have installed the required libraries and have a MySQL server running with the correct user credentials.
2. Save the provided code in a Python file, e.g., `budget_app.py`.
3. Open the terminal or command prompt and navigate to the directory containing the `budget_app.py` file.
4. Run the application using the following command:

```bash
python budget_app.py
```

5. The application window will open, prompting you to log in or register.

### Logging In

- If you already have an account, enter your username and password and click the "Login" button.
- If you don't have an account, click on the "register" link, and the registration window will open.

### Registering

- In the registration window, enter a unique username, a valid email address, and a password.
- Click the "Register" button to create a new account.
- After successful registration, you will be redirected to the login screen.

### Main App

- Once logged in, the main app window will appear.
- The app displays your username and a form to add income or expense transactions.
- Enter the amount and notes for the transaction, then click either "Add Income" or "Add Expense."
- The app will update the total money label and the transaction history.

### Export and Import

- To export the transaction history to an Excel file, click the "Export" button. You can select the file location and name.
- To import transaction history from an Excel file, click the "Import" button and select the file to import.
- The imported transactions will be added to the existing ones, and the total money label will be updated.

### Saving Transactions

- To save the transactions to the database, click the "Save Transactions" button. This will update the transactions in the database.

### Logging Out

- To log out, click the "Log out" button. You will be redirected to the login screen.

## Note

- The application will create a database called "budget_app" if it doesn't already exist. If you have an existing database with the same name, it won't be affected.
- The "users" table will be created if it doesn't exist, and it will store user account details and their transaction history.

Please note that this application is a simple example and may not have robust security measures. It is recommended to enhance the security features before deploying it in a production environment.

Enjoy budgeting with the Budget Management App!