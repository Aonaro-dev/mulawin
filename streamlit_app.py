import streamlit as st
import firebase_admin  # Import firebase_admin
import pyrebase
from firebase_admin import credentials, firestore
import json
import os

# Extract the Firebase credentials from Streamlit secrets and convert to a regular dict
firebase_credentials = dict(st.secrets["firebase"])  # Convert AttrDict to a dict

# Check if the Firebase app is already initialized
if not firebase_admin._apps:
    
    cred = credentials.Certificate(firebase_credentials)
    firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

# Example Firestore document write
def add_data():
    doc_ref = db.collection("users").document("sample_user")
    doc_ref.set({
        "name": "John Doe",
        "age": 30,
        "email": "johndoe@example.com"
    })
    st.write("Data added to Firestore")

if st.button("Add Data"):
    add_data()


firebase_config = {
    "apiKey": st.secrets["firebase"]["apiKey"],
    "authDomain": st.secrets["firebase"]["authDomain"],
    "projectId": st.secrets["firebase"]["projectId"],
    "storageBucket": st.secrets["firebase"]["storageBucket"],
    "messagingSenderId": st.secrets["firebase"]["messagingSenderId"],
    "appId": st.secrets["firebase"]["appId"],
    "measurementId": st.secrets["firebase"]["measurementId"],
    "databaseURL": ""
}

# Initialize pyrebase app
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

# Streamlit app for login
st.title("Login with Google")

# Get authentication
login_button = st.button("Login with Google")

if login_button:
    # Use Firebase's Google Auth Popup method
    # This will open the Firebase Auth sign-in popup
    try:
        user = auth.sign_in_with_google()
        st.write(f"Welcome {user['email']}!")
    except Exception as e:
        st.error(f"Error during sign-in: {e}")
