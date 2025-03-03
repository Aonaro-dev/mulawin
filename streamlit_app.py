import streamlit as st
from authlib.integrations.requests_client import OAuth2Session
import firebase_admin
from firebase_admin import credentials, auth

# Firebase credentials (make sure this is set up correctly)
firebase_credentials = dict(st.secrets["firebase"])

# Initialize Firebase Admin if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_credentials)
    firebase_admin.initialize_app(cred)

def login():
    st.title("Login Page")

    email = st.text_input("Enter your email")
    password = st.text_input("Enter your password", type="password")

    if st.button("Login"):
        try:
            # Sign in with Firebase Auth
            user = auth_client.sign_in_with_email_and_password(email, password)
            st.success("Login successful!")
            st.write(f"Welcome {user['email']}")

        except:
            st.error("Login failed. Please check your credentials.")

def sign_up():
    st.title("Sign Up")

    email = st.text_input("Enter your email")
    password = st.text_input("Enter your password", type="password")

    if st.button("Sign Up"):
        try:
            # Create a new user with Firebase Auth
            user = auth_client.create_user_with_email_and_password(email, password)
            st.success("Account created successfully!")
            st.write(f"Welcome {user['email']}")

        except:
            st.error("Sign up failed. Please try again.")

# Streamlit sidebar for navigation
page = st.sidebar.selectbox("Select Page", ["Login", "Sign Up"])

if page == "Login":
    login()
elif page == "Sign Up":
    sign_up()
