import streamlit as st
import pyrebase
from firebase_admin import credentials, firestore
import firebase_admin

# Firebase configuration
firebaseConfig = {
    "apiKey": st.secrets["firebase"]["apiKey"],
    "authDomain": st.secrets["firebase"]["authDomain"],
    "databaseURL": st.secrets["firebase"]["databaseURL"],
    "projectId": st.secrets["firebase"]["projectId"],
    "storageBucket": st.secrets["firebase"]["storageBucket"],
    "messagingSenderId": st.secrets["firebase"]["messagingSenderId"],
    "appId": st.secrets["firebase"]["appId"],
    "measurementId": st.secrets["firebase"]["measurementId"]
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebaseConfig)
auth_client = firebase.auth()

# Initialize Firebase Admin
if not firebase_admin._apps:
    cred = credentials.Certificate(dict(st.secrets["firebase"]))
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'role' not in st.session_state:
    st.session_state.role = None

# Function to handle login
def login():
    st.title("Login Page")
    email = st.text_input("Enter your email")
    password = st.text_input("Enter your password", type="password")

    if st.button("Login"):
        if not email or not password:
            st.warning("Please enter both email and password.")
        else:
            try:
                # Firebase login
                user = auth_client.sign_in_with_email_and_password(email, password)
                user_id = user['localId']

                # Fetch user data from Firestore
                user_doc = db.collection("users").document(user_id).get()

                if user_doc.exists:
                    user_data = user_doc.to_dict()
                    approved = user_data.get("approved", False)
                    role = user_data.get("role", "user")

                    if role == "admin" or approved:
                        st.session_state.logged_in = True
                        st.session_state.role = role
                        st.experimental_rerun()  # Refresh the page
                    else:
                        st.error("Your account is not approved yet. Please contact the admin.")
                else:
                    st.error("User not found in the database.")
            except Exception as e:
                st.error(f"Login failed. Error: {str(e)}")

# Function to handle signup
def sign_up():
    st.title("Sign Up")
    email = st.text_input("Enter your email")
    password = st.text_input("Enter your password", type="password")

    if st.button("Sign Up"):
        try:
            # Create a new user
            user = auth_client.create_user_with_email_and_password(email, password)
            user_id = user['localId']

            # Add user to Firestore
            db.collection("users").document(user_id).set({
                "email": email,
                "approved": False,
                "role": "user"
            })

            st.success("Account created. Wait for admin approval.")
        except Exception as e:
            st.error(f"Sign up failed. Error: {str(e)}")

# Routing logic
if st.session_state.logged_in:
    # Show the sidebar for logged-in users
    st.sidebar.success(f"Logged in as {st.session_state.role.capitalize()}")

    if st.session_state.role == "admin":
        st.sidebar.button("Go to Admin Page", on_click=lambda: st.switch_page("admin"))
    else:
        st.sidebar.button("Go to Main Page", on_click=lambda: st.switch_page("main"))

    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.experimental_rerun()

else:
    # Sidebar for login and signup
    st.sidebar.title("User Authentication")
    action = st.sidebar.radio("Select Action", ["Login", "Sign Up"])

    if action == "Login":
        login()
    elif action == "Sign Up":
        sign_up()
