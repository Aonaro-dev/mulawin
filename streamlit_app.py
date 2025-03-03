import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, db
import pyrebase

# Access secrets from Streamlit Secrets
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

# Initialize Firebase app for client-side
firebase = pyrebase.initialize_app(firebaseConfig)
auth_client = firebase.auth()

# Firebase credentials
firebase_credentials = dict(st.secrets["firebase"])

# Initialize Firebase Admin if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_credentials)
    firebase_admin.initialize_app(cred, {'databaseURL': firebaseConfig['databaseURL']})

# Firebase Database reference for user data
ref = db.reference("/users")

def login():
    st.title("Login Page")

    email = st.text_input("Enter your email")
    password = st.text_input("Enter your password", type="password")

    if st.button("Login"):
        try:
            # Sign in with Firebase Auth
            user = auth_client.sign_in_with_email_and_password(email, password)
            user_id = user['localId']

            # Check if the user is approved
            user_data = ref.child(user_id).get()

            if user_data and user_data.get("approved", False):
                st.success("Login successful!")
                st.write(f"Welcome {user['email']}")
                st.experimental_set_query_params(logged_in="true")
                st.switch_page("main")
            else:
                st.error("Your account is not approved yet. Please contact the admin.")

        except Exception as e:
            st.error(f"Login failed. Error: {e}")

def sign_up():
    st.title("Sign Up")

    email = st.text_input("Enter your email")
    password = st.text_input("Enter your password", type="password")

    if st.button("Sign Up"):
        try:
            # Create a new user with Firebase Auth
            user = auth_client.create_user_with_email_and_password(email, password)
            user_id = user['localId']

            # Store user details in Firebase Database with approval set to False
            ref.child(user_id).set({
                "email": email,
                "approved": False
            })

            st.success("Account created successfully! Please wait for admin approval.")
            st.write(f"Welcome {user['email']}")

        except Exception as e:
            st.error(f"Sign up failed. Error: {e}")

# Streamlit sidebar for navigation
page = st.sidebar.selectbox("Select Page", ["Login", "Sign Up"])

if page == "Login":
    login()
elif page == "Sign Up":
    sign_up()
