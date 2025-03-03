import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, auth
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
    firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

def login():
    st.title("Login Page")

    email = st.text_input("Enter your email")
    password = st.text_input("Enter your password", type="password")

    if st.button("Login"):
        if not email or not password:
            st.warning("Please enter both email and password.")
        else:
            try:
                # Sign in with Firebase Auth
                user = auth_client.sign_in_with_email_and_password(email, password)
                user_id = user['localId']

                # Check if the user is approved in Firestore
                user_doc = db.collection("users").document(user_id).get()

                if user_doc.exists and user_doc.to_dict().get("approved", False):
                    st.success("Login successful!")
                    st.write(f"Welcome {user['email']}")
                    st.experimental_set_query_params(logged_in="true")
                    st.switch_page("main")
                else:
                    st.error("Your account is not approved yet. Please contact the admin.")

            except Exception as e:
                # Handle specific errors based on error message
                error_message = str(e)
                if "INVALID_LOGIN_CREDENTIALS" in error_message:
                    st.error("Invalid login credentials. Please check your email and password.")
                elif "EMAIL_NOT_FOUND" in error_message:
                    st.error("Email not found. Please sign up first.")
                else:
                    st.error(f"Login failed. Error: {error_message}")


def sign_up():
    st.title("Sign Up")

    email = st.text_input("Enter your email")
    password = st.text_input("Enter your password", type="password")

    if st.button("Sign Up"):
        try:
            # Create a new user with Firebase Auth
            user = auth_client.create_user_with_email_and_password(email, password)
            user_id = user['localId']

            # Check if this is the first user (admin)
            users_ref = db.collection("users").get()
            is_admin = len(users_ref) == 0  # First user becomes admin

            # Store user details in Firestore with approval set to False and admin role if first user
            db.collection("users").document(user_id).set({
                "email": email,
                "approved": False,
                "role": "admin" if is_admin else "user"  # First user is admin, others are normal users
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
