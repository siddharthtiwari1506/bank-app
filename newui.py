from pathlib import Path
import json
import random
import string
import tkinter as tk
from tkinter import messagebox, simpledialog

# --- Bank Class Definition (Modified for better integration) ---

class Bank:
    # Class attributes for database management
    database = 'database.json'
    data = []

    # Initialize and load data upon class definition
    try: 
        if Path(database).exists():
            with open(database) as fs:
                # Load existing data, defaulting to an empty list if file is empty
                content = fs.read()
                data = json.loads(content) if content else []
        else:
            # If database.json doesn't exist, it will be created on the first update
            print("Database file not found. A new one will be created.")

    except Exception as err:
        print(f"An error occurred while loading data: {err}")

    @classmethod
    def __update(cls):
        """Saves the current state of cls.data back to the database file."""
        try:
            with open(cls.database, 'w') as fs:
                json.dump(cls.data, fs, indent=4) # Use json.dump for better writing and indent for readability
        except Exception as err:
            messagebox.showerror("Database Error", f"Could not update database: {err}")
            return False
        return True
    
    @staticmethod
    def __accountno():
        """Generates a unique 9-character alphanumeric account number."""
        alpha = random.choices(string.ascii_letters, k=5)
        digits = random.choices(string.digits, k=4)
        id_list = alpha + digits
        random.shuffle(id_list)
        return "".join(id_list)

    @classmethod
    def create_account(cls, name, email, phone_no, pin):
        """Creates a new account and saves it."""
        try:
            phone_no = int(phone_no)
            pin = int(pin)
        except ValueError:
            return "Error: Phone number and PIN must be numeric."

        if len(str(pin)) != 4:
            return "Error: PIN must be exactly 4 digits."
        
        if len(str(phone_no)) != 10:
            return "Error: Phone number must be exactly 10 digits."

        d = {
            "name": name,
            "email": email,
            "phone no.": phone_no,
            "pin": pin,
            "Account no.": Bank.__accountno(),
            "Balance": 0        
        }
        
        cls.data.append(d)
        if cls.__update():
            return f"Success! Account created. Account No: {d['Account no.']}"
        else:
            return "Error: Account created locally but failed to save to database."

    @classmethod
    def __find_user(cls, accNo, pin):
        """Utility to find a user by account number and pin."""
        try:
            pin = int(pin)
        except ValueError:
            return None # Pin is not an integer

        # Find the specific user dictionary in the data list
        user_data = next((i for i in cls.data if i['Account no.'] == accNo and i['pin'] == pin), None)
        return user_data

    @classmethod
    def deposit_money(cls, accNo, pin, amount):
        """Deposits money into an account."""
        user_data = cls.__find_user(accNo, pin)
        if not user_data:
            return "Error: User not found or incorrect PIN."
        
        try:
            amount = int(amount)
        except ValueError:
            return "Error: Amount must be numeric."

        if amount <= 0:
            return "Error: Invalid amount. Must be positive."
        elif amount > 100000:
            return "Error: Deposit limit is 100,000."
        else:
            user_data['Balance'] += amount
            if cls.__update():
                return f"Success! Amount credited. New Balance: {user_data['Balance']}"
            else:
                return "Error: Deposit successful locally but failed to save to database."

    @classmethod
    def withdraw_money(cls, accNo, pin, amount):
        """Withdraws money from an account."""
        user_data = cls.__find_user(accNo, pin)
        if not user_data:
            return "Error: User not found or incorrect PIN."

        try:
            amount = int(amount)
        except ValueError:
            return "Error: Amount must be numeric."
        
        if amount <= 0:
            return "Error: Invalid amount. Must be positive."
        elif amount > 10000:
            return "Error: Withdrawal limit is 10,000."
        elif amount > user_data['Balance']:
            return "Error: Insufficient balance."
        else:
            user_data['Balance'] -= amount
            if cls.__update():
                return f"Success! Amount debited. New Balance: {user_data['Balance']}"
            else:
                return "Error: Withdrawal successful locally but failed to save to database."

    @classmethod
    def get_details(cls, accNo, pin):
        """Retrieves and formats account details."""
        user_data = cls.__find_user(accNo, pin)
        if not user_data:
            return "Error: User not found or incorrect PIN."
        
        details_str = ""
        for k, v in user_data.items():
            details_str += f"**{k}:** {v}\n"
        return details_str

    @classmethod
    def delete_account(cls, accNo, pin):
        """Deletes an account permanently."""
        user_data = cls.__find_user(accNo, pin)
        if not user_data:
            return "Error: User not found or incorrect PIN."
        
        # Remove the user dictionary from the class data list
        cls.data.remove(user_data)
        
        if cls.__update():
            return "Success! Account deleted successfully."
        else:
            return "Error: Account deleted locally but failed to save to database."

# --- Tkinter GUI Implementation ---

class BankGUI:
    def __init__(self, master):
        self.master = master
        master.title("🏦 Simple Banking System")

        # Set up a main frame for padding and structure
        self.main_frame = tk.Frame(master, padx=10, pady=10)
        self.main_frame.pack(fill='both', expand=True)

        # Title Label
        self.title_label = tk.Label(self.main_frame, text="Bank Operations Menu", font=('Arial', 16, 'bold'))
        self.title_label.pack(pady=10)

        # Button Setup (using lambda functions to call methods)
        button_info = [
            ("1. Create Account", self.show_create_account_form),
            ("2. Deposit Money", lambda: self.show_transaction_form("Deposit")),
            ("3. Withdraw Money", lambda: self.show_transaction_form("Withdraw")),
            ("4. View Details", self.show_details_form),
            ("5. Delete Account", self.show_delete_account_form),
        ]

        for text, command in button_info:
            tk.Button(self.main_frame, text=text, command=command, width=30, height=2, bg='lightblue').pack(pady=5)

    def show_create_account_form(self):
        """Opens a dialog for creating a new account."""
        
        def submit_creation():
            """Handles the submission of the create account form."""
            name = entry_name.get()
            email = entry_email.get()
            phone = entry_phone.get()
            pin = entry_pin.get()

            # Input validation (basic check for empty fields)
            if not all([name, email, phone, pin]):
                messagebox.showerror("Input Error", "All fields must be filled.")
                return

            result = Bank.create_account(name, email, phone, pin)
            
            # Close the dialog and display the result
            create_win.destroy()
            if "Error" in result:
                messagebox.showerror("Account Creation Failed", result)
            else:
                messagebox.showinfo("Account Created", result)

        create_win = tk.Toplevel(self.master)
        create_win.title("Create New Account")
        create_win.geometry("300x300")
        
        tk.Label(create_win, text="Name:").pack(pady=2)
        entry_name = tk.Entry(create_win)
        entry_name.pack(pady=2)

        tk.Label(create_win, text="Email:").pack(pady=2)
        entry_email = tk.Entry(create_win)
        entry_email.pack(pady=2)
        
        tk.Label(create_win, text="Phone No (10 digits):").pack(pady=2)
        entry_phone = tk.Entry(create_win)
        entry_phone.pack(pady=2)

        tk.Label(create_win, text="PIN (4 digits):").pack(pady=2)
        entry_pin = tk.Entry(create_win, show="*") # Hide PIN input
        entry_pin.pack(pady=2)

        tk.Button(create_win, text="Submit", command=submit_creation).pack(pady=10)

    def show_transaction_form(self, operation_type):
        """Opens a dialog for Deposit or Withdraw operations."""

        def submit_transaction():
            """Handles the submission of the transaction form."""
            acc_no = entry_accNo.get()
            pin = entry_pin.get()
            amount = entry_amount.get()

            if not all([acc_no, pin, amount]):
                messagebox.showerror("Input Error", "Account No, PIN, and Amount must be filled.")
                return

            # Call the appropriate Bank method
            if operation_type == "Deposit":
                result = Bank.deposit_money(acc_no, pin, amount)
            elif operation_type == "Withdraw":
                result = Bank.withdraw_money(acc_no, pin, amount)
            else:
                result = "Internal Error: Invalid operation type."
            
            trans_win.destroy()
            if "Error" in result:
                messagebox.showerror(f"{operation_type} Failed", result)
            else:
                messagebox.showinfo(f"{operation_type} Successful", result)


        trans_win = tk.Toplevel(self.master)
        trans_win.title(f"{operation_type} Money")
        trans_win.geometry("300x200")

        tk.Label(trans_win, text="Account No:").pack(pady=2)
        entry_accNo = tk.Entry(trans_win)
        entry_accNo.pack(pady=2)

        tk.Label(trans_win, text="PIN:").pack(pady=2)
        entry_pin = tk.Entry(trans_win, show="*")
        entry_pin.pack(pady=2)

        tk.Label(trans_win, text="Amount:").pack(pady=2)
        entry_amount = tk.Entry(trans_win)
        entry_amount.pack(pady=2)

        tk.Button(trans_win, text=operation_type, command=submit_transaction).pack(pady=10)

    def show_details_form(self):
        """Opens a dialog to view account details."""

        def submit_details():
            """Handles the submission for viewing details."""
            acc_no = entry_accNo.get()
            pin = entry_pin.get()

            if not all([acc_no, pin]):
                messagebox.showerror("Input Error", "Account No and PIN must be filled.")
                return

            result = Bank.get_details(acc_no, pin)
            
            details_win.destroy()
            if "Error" in result:
                messagebox.showerror("Details Failed", result)
            else:
                # Use a custom Toplevel for displaying multiline/formatted details
                info_win = tk.Toplevel(self.master)
                info_win.title("Account Details")
                tk.Label(info_win, text="--- Account Information ---", font=('Arial', 12, 'bold')).pack(pady=5)
                # Use a Label for display, with justified text alignment
                tk.Label(info_win, text=result, justify=tk.LEFT, padx=10, pady=10).pack()
                tk.Button(info_win, text="Close", command=info_win.destroy).pack(pady=10)


        details_win = tk.Toplevel(self.master)
        details_win.title("View Account Details")
        details_win.geometry("300x150")

        tk.Label(details_win, text="Account No:").pack(pady=2)
        entry_accNo = tk.Entry(details_win)
        entry_accNo.pack(pady=2)

        tk.Label(details_win, text="PIN:").pack(pady=2)
        entry_pin = tk.Entry(details_win, show="*")
        entry_pin.pack(pady=2)

        tk.Button(details_win, text="Get Details", command=submit_details).pack(pady=10)

    def show_delete_account_form(self):
        """Opens a dialog to delete an account."""
        
        def submit_delete():
            """Handles the submission for deleting the account."""
            acc_no = entry_accNo.get()
            pin = entry_pin.get()

            if not all([acc_no, pin]):
                messagebox.showerror("Input Error", "Account No and PIN must be filled.")
                return
            
            # Confirmation dialog for security
            if not messagebox.askyesno("Confirm Deletion", "Are you sure you want to permanently delete this account? This action cannot be undone."):
                delete_win.destroy()
                return

            result = Bank.delete_account(acc_no, pin)
            
            delete_win.destroy()
            if "Error" in result:
                messagebox.showerror("Deletion Failed", result)
            else:
                messagebox.showinfo("Account Deleted", result)

        delete_win = tk.Toplevel(self.master)
        delete_win.title("Delete Account")
        delete_win.geometry("300x150")

        tk.Label(delete_win, text="Account No:").pack(pady=2)
        entry_accNo = tk.Entry(delete_win)
        entry_accNo.pack(pady=2)

        tk.Label(delete_win, text="PIN:").pack(pady=2)
        entry_pin = tk.Entry(delete_win, show="*")
        entry_pin.pack(pady=2)

        tk.Button(delete_win, text="Delete Account", bg='red', fg='white', command=submit_delete).pack(pady=10)


# Main Tkinter Loop
if __name__ == '__main__':
    root = tk.Tk()
    app = BankGUI(root)
    root.mainloop()