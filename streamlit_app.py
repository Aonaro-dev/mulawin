import streamlit as st
from firebase_admin import credentials, firestore
import json
import os

# Extract the Firebase credentials from Streamlit secrets
firebase_credentials = st.secrets["firebase"]

# Save the credentials as a temporary JSON file
with open("firebase_credentials.json", "w") as f:
    json.dump(firebase_credentials, f)

# Initialize Firebase with the temporary JSON file
cred = credentials.Certificate("firebase_credentials.json")
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

# Remove the temporary JSON file after use
os.remove("firebase_credentials.json")
