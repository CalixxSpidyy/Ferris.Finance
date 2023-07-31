import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import pandas as pd
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
from ttkthemes import ThemedStyle
import mysql.connector
import re
import json


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        return super().default(o)


class BudgetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Management App")

        self.username = None
        self.logged_in = False

        self.total_money = 0
        self.transactions = []

        if not self.logged_in:
            self.show_login_screen()
            self.create_database()
            self.create_users_table()
        else:
            self.show_main_app()

        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Codegeassr1721!",
            database="budget_app"
        )
        self.cursor = self.connection.cursor()

    def create_database(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Codegeassr1721!"
            )
            cursor = connection.cursor()

            create_db_query = "CREATE DATABASE IF NOT EXISTS budget_app;"

            cursor.execute(create_db_query)
            cursor.close()
            connection.commit()
            connection.close()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"An error occurred while creating the database: {err}")

    def create_users_table(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Codegeassr1721!",
                database="budget_app"
            )
            cursor = connection.cursor()

            create_table_query = """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL UNIQUE,
                email VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL
            )
            """

            cursor.execute(create_table_query)
            cursor.close()
            connection.commit()
            connection.close()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"An error occurred while creating the 'users' table: {err}")

    def close_app(self):
        self.root.destroy()

    def show_login_screen(self):
        self.root.withdraw()

        self.login_window = tk.Toplevel(self.root)
        self.login_window.title("Login")
        self.login_window.geometry("300x150")

        self.label_username = tk.Label(self.login_window, text="Username:")
        self.label_username.grid(row=0, column=0, padx=5, pady=5)
        self.entry_username = tk.Entry(self.login_window)
        self.entry_username.grid(row=0, column=1, padx=5, pady=5)

        self.label_password = tk.Label(self.login_window, text="Password:")
        self.label_password.grid(row=1, column=0, padx=5, pady=5)
        self.entry_password = tk.Entry(self.login_window, show="*")
        self.entry_password.grid(row=1, column=1, padx=5, pady=5)

        self.btn_login = tk.Button(self.login_window, text="Login", command=self.login)
        self.btn_login.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

        self.label_clickable_text = tk.Label(self.login_window, text="register", fg="blue", cursor="hand2")
        self.label_clickable_text.grid(row=3, column=0, columnspan=2)
        self.label_clickable_text.bind("<Button-1>", self.open_register_window)

        self.login_window.protocol("WM_DELETE_WINDOW", self.close_app)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        try:
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            self.cursor.execute(query, (username, password))
            result = self.cursor.fetchone()

            if result:
                self.username = username
                self.logged_in = True

                transactions_json = result[4]

                print("Received transactions JSON:", transactions_json)

                try:
                    self.transactions = json.loads(transactions_json, object_hook=self._datetime_decoder) if transactions_json else []

                    for i, (amount, timestamp, notes) in enumerate(self.transactions):
                        self.transactions[i] = (amount, datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S"), notes)

                    if not isinstance(self.transactions, list):
                        self.transactions = []

                except json.JSONDecodeError:
                    self.transactions = []
                    messagebox.showerror("Login Error", "Error loading transactions data. Please contact support.")
                    self.entry_password.delete(0, tk.END)
                    return

                self.login_window.destroy()
                self.root.deiconify()
                self.show_main_app()

            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")
                self.entry_password.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Login Error", f"An error occurred during login: {e}")
            self.entry_password.delete(0, tk.END)

    def _datetime_decoder(self, dct):
        if 'Datetime' in dct:
            dct['Datetime'] = datetime.strptime(dct['Datetime'], "%Y-%m-%d %H:%M:%S")
        return dct

    def logout(self):
        self.label_welcome.destroy()
        self.label_income_expense.destroy()
        self.entry_income_expense.destroy()
        self.label_notes.destroy()
        self.entry_notes.destroy()
        self.btn_add_income.destroy()
        self.btn_add_expense.destroy()
        self.label_total.destroy()
        self.label_total_money.destroy()
        self.tree.destroy()
        self.btn_export.destroy()
        self.btn_import.destroy()
        self.btn_save_transactions.destroy()
        self.btn_logout.destroy()

        self.username = None
        self.logged_in = False

        self.show_login_screen()

    def open_register_window(self, event):
        self.root.withdraw()
        self.login_window.destroy()
        self.register_window = tk.Toplevel(self.root)
        self.register_window.title("Register")
        self.register_window.geometry("300x150")

        self.label_register_username = tk.Label(self.register_window, text="Username:")
        self.label_register_username.grid(row=0, column=0, padx=5, pady=5)
        self.entry_register_username = tk.Entry(self.register_window)
        self.entry_register_username.grid(row=0, column=1, padx=5, pady=5)

        self.label_register_email = tk.Label(self.register_window, text="Email:")
        self.label_register_email.grid(row=1, column=0, padx=5, pady=5)
        self.entry_register_email = tk.Entry(self.register_window)
        self.entry_register_email.grid(row=1, column=1, padx=5, pady=5)

        self.label_register_password = tk.Label(self.register_window, text="Password:")
        self.label_register_password.grid(row=2, column=0, padx=5, pady=5)
        self.entry_register_password = tk.Entry(self.register_window, show="*")
        self.entry_register_password.grid(row=2, column=1, padx=5, pady=5)

        self.btn_register = tk.Button(self.register_window, text="Register", command=self.register)
        self.btn_register.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

        self.label_clickable_text = tk.Label(self.register_window, text="Login", fg="blue", cursor="hand2")
        self.label_clickable_text.grid(row=4, column=0, columnspan=2)
        self.label_clickable_text.bind("<Button-1>", self.open_login_window)

        self.register_window.protocol("WM_DELETE_WINDOW", self.close_app)

    def open_login_window(self, event):
        self.register_window.destroy()
        self.show_login_screen()

    def validate_email(self, email):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email)

    def register(self):
        username = self.entry_register_username.get()
        email = self.entry_register_email.get()
        password = self.entry_register_password.get()

        if not self.validate_email(email):
            messagebox.showerror("Invalid Email", "Please enter a valid email address.")
            return

        try:
            query = "SELECT * FROM users WHERE username = %s OR email = %s"
            self.cursor.execute(query, (username, email))
            result = self.cursor.fetchall()

            if result:
                messagebox.showerror("User Already Exists", "Username or email already registered.")
                return

            transactions = []
            transactions_json = json.dumps(transactions)

            query = "INSERT INTO users (username, email, password, transactions) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(query, (username, email, password, transactions_json))
            self.connection.commit()

            messagebox.showinfo("Registration Successful", "Registration successful.")
            self.register_window.destroy()
            self.show_login_screen()

        except Exception as e:
            messagebox.showerror("Registration Error", f"An error occurred during registration:\n{e}")
            print(e)

    def show_main_app(self):
        self.label_welcome = tk.Label(self.root, text=f"Hello {self.username}")
        self.label_welcome.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        self.label_income_expense = tk.Label(self.root, text="Amount:")
        self.label_income_expense.grid(row=1, column=0, padx=5, pady=5)
        self.entry_income_expense = tk.Entry(self.root)
        self.entry_income_expense.grid(row=1, column=1, padx=5, pady=5)

        self.label_notes = tk.Label(self.root, text="Notes:")
        self.label_notes.grid(row=2, column=0, padx=5, pady=5)
        self.entry_notes = tk.Entry(self.root)
        self.entry_notes.grid(row=2, column=1, padx=5, pady=5)

        self.btn_add_income = tk.Button(self.root, text="Add Income", command=self.add_income)
        self.btn_add_income.grid(row=3, column=0, padx=5, pady=5)

        self.btn_add_expense = tk.Button(self.root, text="Add Expense", command=self.add_expense)
        self.btn_add_expense.grid(row=3, column=1, padx=5, pady=5)

        self.label_total = tk.Label(self.root, text="Total Money:")
        self.label_total.grid(row=4, column=0, padx=5, pady=5)
        self.label_total_money = tk.Label(self.root, text=str(self.total_money))
        self.label_total_money.grid(row=4, column=1, padx=5, pady=5)

        self.tree = ttk.Treeview(self.root, columns=("Income", "Datetime", "Notes"), show="headings")
        self.tree.heading("Income", text="Income")
        self.tree.heading("Datetime", text="Datetime")
        self.tree.heading("Notes", text="Notes")
        self.tree.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        self.btn_export = tk.Button(self.root, text="Export", command=self.export_to_excel)
        self.btn_export.grid(row=6, column=0, padx=5, pady=5)

        self.btn_import = tk.Button(self.root, text="Import", command=self.import_from_excel)
        self.btn_import.grid(row=6, column=1, padx=5, pady=5)

        self.btn_save_transactions = tk.Button(self.root, text="Save Transactions", command=self.save_transactions)
        self.btn_save_transactions.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

        self.btn_logout = tk.Button(self.root, text="Log out", command=self.logout)
        self.btn_logout.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

        self.update_transaction_history()
        self.calculate_total_amount()

    def add_income(self):
        try:
            income = float(self.entry_income_expense.get())
            notes = self.entry_notes.get()
            self.total_money += income
            self.update_total_money_label()
            self.entry_income_expense.delete(0, tk.END)
            self.entry_notes.delete(0, tk.END)
            self.add_transaction(income, notes)
        except ValueError:
            pass

    def add_expense(self):
        try:
            expense = float(self.entry_income_expense.get())
            notes = self.entry_notes.get()
            self.total_money -= abs(expense)
            self.update_total_money_label()
            self.entry_income_expense.delete(0, tk.END)
            self.entry_notes.delete(0, tk.END)
            self.add_transaction(-expense, notes)
        except ValueError:
            pass

    def calculate_total_amount(self):
        self.total_money = sum(amount for amount, _, _ in self.transactions)
        self.update_total_money_label()

    def update_total_money_label(self):
        self.label_total_money.config(text=str(self.total_money))

    def add_transaction(self, amount, notes):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transactions.append((amount, timestamp, notes))
        self.update_transaction_history()

    def update_transaction_history(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for amount, timestamp, notes in self.transactions:
            self.tree.insert("", "end", values=(amount, timestamp, notes))

    def export_to_excel(self):
        if not self.transactions:
            return

        df = pd.DataFrame(self.transactions, columns=["Income", "Datetime", "Notes"])

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")],
            title="Save Transaction History"
        )

        if file_path:
            try:
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Export Successful", "Transaction history exported to Excel.")
            except Exception as e:
                messagebox.showerror("Export Error", f"An error occurred during export:\n{e}")

    def import_from_excel(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")],
            title="Select Transaction History File to Import"
        )

        if file_path:
            try:
                df = pd.read_excel(file_path)

                self.transactions.clear()
                self.update_transaction_history()

                for _, row in df.iterrows():
                    income = row["Income"]
                    timestamp_str = str(row["Datetime"])
                    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                    notes = row["Notes"]
                    self.transactions.append((income, timestamp, notes))

                self.update_transaction_history()
                messagebox.showinfo("Import Successful", "Transaction history imported from Excel.")
            except Exception as e:
                messagebox.showerror("Import Error", f"An error occurred during import:\n{e}")

        self.calculate_total_amount()

    def save_transactions(self):
        try:
            transactions_json = json.dumps(self.transactions, cls=DateTimeEncoder)

            query = "UPDATE users SET transactions = %s WHERE username = %s"
            self.cursor.execute(query, (transactions_json, self.username))
            self.connection.commit()

            messagebox.showinfo("Save Successful", "Transaction history saved.")
            self.update_transaction_history()
        except Exception as e:
            messagebox.showerror("Save Error", f"An error occurred while saving transactions: {e}")

    def __del__(self):
        self.cursor.close()
        self.connection.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetApp(root)
    root.mainloop()
