import streamlit as st

# Access credentials from secrets
user_credentials = st.secrets["user"]
admin_credentials = st.secrets["admin"]

# Create the login form
st.title("Login Page")

# Get input from the user
username = st.text_input("Enter your username")
password = st.text_input("Enter your password", type="password")

# Initialize the session state
if 'login_status' not in st.session_state:
    st.session_state['login_status'] = False
    st.session_state['user_role'] = None

# Function to validate credentials
def validate_login(username, password):
    if username == user_credentials["username"] and password == user_credentials["password"]:
        return "user"
    elif username == admin_credentials["username"] and password == admin_credentials["password"]:
        return "admin"
    else:
        return None

# Validate credentials when user clicks the login button
if st.button("Login"):
    role = validate_login(username, password)
    
    if role:
        st.session_state['login_status'] = True
        st.session_state['user_role'] = role
        st.success(f"Logged in as {role}")
    else:
        st.error("Invalid credentials. Please try again.")

# If logged in, show the main content
if st.session_state['login_status']:
    if st.session_state['user_role'] == 'admin':
        st.write("Welcome, Admin! Here is your dashboard...")
        # Add your admin dashboard or functionality here
    else:
        st.write("Welcome, User! Here is your content...")
        # Add your user-specific functionality here
