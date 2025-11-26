import streamlit as st
import json
import random
import string
import os

# --- Constants ---
DATABASE_FILE = 'database.json'

# --- Backend Logic (Refactored for Streamlit) ---
class BankSystem:
    """
    A helper class to manage bank operations. 
    Adapted from the original code to separate logic from the UI.
    """
    
    @staticmethod
    def load_data():
        if os.path.exists(DATABASE_FILE):
            try:
                with open(DATABASE_FILE, 'r') as f:
                    content = f.read()
                    if content:
                        return json.loads(content)
            except Exception as e:
                st.error(f"Error loading database: {e}")
        return []

    @staticmethod
    def save_data(data):
        try:
            with open(DATABASE_FILE, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            st.error(f"Error saving database: {e}")
            return False

    @staticmethod
    def generate_account_no():
        alpha = random.choices(string.ascii_letters, k=5)
        digits = random.choices(string.digits, k=4)
        id_list = alpha + digits
        random.shuffle(id_list)
        return "".join(id_list)

    @staticmethod
    def find_user(data, acc_no, pin):
        """Finds a user and returns the index and the user dict."""
        for index, user in enumerate(data):
            # Convert pin to int for comparison as JSON stores/loads inputs
            if user['Account no.'] == acc_no and str(user['pin']) == str(pin):
                return index, user
        return -1, None

# --- Streamlit UI ---

def main():
    st.set_page_config(page_title="Python Bank", page_icon="🏦", layout="centered")

    st.title("🏦 Python Bank System")
    
    # Sidebar Navigation
    menu = ["Home", "Create Account", "Deposit Money", "Withdraw Money", "Account Details", "Update Details", "Delete Account"]
    choice = st.sidebar.selectbox("Menu", menu)

    # Load current data
    data = BankSystem.load_data()

    if choice == "Home":
        st.markdown("""
        ### Welcome to Python Bank
        Please use the sidebar to navigate through the operations.
        
        * **Secure**: Pin protection enabled.
        * **Fast**: Instant updates.
        * **Reliable**: Local JSON storage.
        """)
        st.info(f"Total Accounts in System: {len(data)}")

    # --- Create Account ---
    elif choice == "Create Account":
        st.subheader("📝 Create New Account")
        
        with st.form("create_form"):
            name = st.text_input("Full Name")
            email = st.text_input("Email Address")
            phone = st.text_input("Phone Number (10 digits)")
            pin = st.text_input("Set 4-Digit PIN", type="password", max_chars=4)
            
            submitted = st.form_submit_button("Create Account")
            
            if submitted:
                # Validation
                if not name or not email:
                    st.error("Name and Email are required.")
                elif len(phone) != 10 or not phone.isnumeric():
                    st.error("Phone number must be exactly 10 digits.")
                elif len(pin) != 4 or not pin.isnumeric():
                    st.error("PIN must be exactly 4 digits.")
                else:
                    # Creation Logic
                    acc_no = BankSystem.generate_account_no()
                    new_user = {
                        "name": name,
                        "email": email,
                        "phone no.": int(phone),
                        "pin": int(pin),
                        "Account no.": acc_no,
                        "Balance": 0
                    }
                    data.append(new_user)
                    if BankSystem.save_data(data):
                        st.success("Account Created Successfully!")
                        st.balloons()
                        st.markdown(f"""
                        <div style="background-color: #d4edda; padding: 10px; border-radius: 5px; color: #155724;">
                            <strong>Your Account Number is:</strong> <span style="font-size: 1.2em; font-weight: bold;">{acc_no}</span><br>
                            Please save this for future transactions.
                        </div>
                        """, unsafe_allow_html=True)

    # --- Deposit Money ---
    elif choice == "Deposit Money":
        st.subheader("💰 Deposit Money")
        
        with st.form("deposit_form"):
            acc_no = st.text_input("Account Number")
            pin = st.text_input("PIN", type="password")
            amount = st.number_input("Amount to Deposit", min_value=1, max_value=100000, step=100)
            
            submitted = st.form_submit_button("Deposit")
            
            if submitted:
                idx, user = BankSystem.find_user(data, acc_no, pin)
                if user:
                    user['Balance'] += amount
                    data[idx] = user # Update list
                    BankSystem.save_data(data)
                    st.success(f"₹{amount} Credited Successfully!")
                    st.info(f"New Balance: ₹{user['Balance']}")
                else:
                    st.error("Authentication Failed! Check Account No. or PIN.")

    # --- Withdraw Money ---
    elif choice == "Withdraw Money":
        st.subheader("💸 Withdraw Money")
        
        with st.form("withdraw_form"):
            acc_no = st.text_input("Account Number")
            pin = st.text_input("PIN", type="password")
            amount = st.number_input("Amount to Withdraw", min_value=1, max_value=10000, step=100)
            
            submitted = st.form_submit_button("Withdraw")
            
            if submitted:
                idx, user = BankSystem.find_user(data, acc_no, pin)
                if user:
                    if user['Balance'] >= amount:
                        user['Balance'] -= amount
                        data[idx] = user
                        BankSystem.save_data(data)
                        st.success(f"₹{amount} Debited Successfully!")
                        st.info(f"Remaining Balance: ₹{user['Balance']}")
                    else:
                        st.error(f"Insufficient Funds! Current Balance: ₹{user['Balance']}")
                else:
                    st.error("Authentication Failed! Check Account No. or PIN.")

    # --- Account Details ---
    elif choice == "Account Details":
        st.subheader("📋 Account Details")
        
        with st.form("details_form"):
            acc_no = st.text_input("Account Number")
            pin = st.text_input("PIN", type="password")
            submitted = st.form_submit_button("Fetch Details")
            
            if submitted:
                idx, user = BankSystem.find_user(data, acc_no, pin)
                if user:
                    st.json(user)
                else:
                    st.error("User not found! Check credentials.")

    # --- Update Details ---
    elif choice == "Update Details":
        st.subheader("🔄 Update Information")
        st.markdown("Enter your login details and the *new* information. Leave fields blank if you don't want to change them.")
        
        with st.form("update_form"):
            col1, col2 = st.columns(2)
            with col1:
                acc_no = st.text_input("Account Number (Login)")
                pin = st.text_input("PIN (Login)", type="password")
            
            st.divider()
            
            with col2:
                new_name = st.text_input("New Name (Optional)")
                new_email = st.text_input("New Email (Optional)")
                new_phone = st.text_input("New Phone (Optional)")
                new_pin = st.text_input("New PIN (Optional)", max_chars=4)

            submitted = st.form_submit_button("Update Profile")
            
            if submitted:
                idx, user = BankSystem.find_user(data, acc_no, pin)
                if user:
                    # Logic from original script: update if new value provided
                    if new_name: user['name'] = new_name
                    if new_email: user['email'] = new_email
                    if new_phone: 
                        if len(new_phone) == 10 and new_phone.isnumeric():
                             user['phone no.'] = int(new_phone)
                        else:
                            st.warning("New phone number ignored (Invalid format).")
                    if new_pin:
                        if len(new_pin) == 4 and new_pin.isnumeric():
                             user['pin'] = int(new_pin)
                        else:
                            st.warning("New PIN ignored (Invalid format).")
                    
                    data[idx] = user
                    BankSystem.save_data(data)
                    st.success("Details Updated Successfully!")
                    st.json(user)
                else:
                    st.error("Authentication Failed. Cannot update.")

    # --- Delete Account ---
    elif choice == "Delete Account":
        st.subheader("❌ Deactivate Account")
        
        with st.form("delete_form"):
            st.warning("This action is permanent and cannot be undone.")
            acc_no = st.text_input("Account Number")
            pin = st.text_input("PIN", type="password")
            
            submitted = st.form_submit_button("Permanently Delete Account")
            
            if submitted:
                idx, user = BankSystem.find_user(data, acc_no, pin)
                if user:
                    del data[idx]
                    BankSystem.save_data(data)
                    st.success("Account Deleted Successfully.")
                else:
                    st.error("Authentication Failed.")

if __name__ == "__main__":
    main()
    