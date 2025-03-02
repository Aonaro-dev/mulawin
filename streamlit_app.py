import streamlit as st
from firebase_admin import credentials, firestore
import json
import os

# Extract the Firebase credentials from Streamlit secrets and convert to a regular dict
firebase_credentials = dict(st.secrets["firebase"])  # Convert AttrDict to a dict

# Write the credentials to a temporary JSON file
with open("firebase_credentials_temp.json", "w") as f:
    json.dump(firebase_credentials, f)

# Initialize Firebase with the temporary JSON file
cred = credentials.Certificate("firebase_credentials_temp.json")
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

# Remove the temporary JSON file after Firebase is initialized
os.remove("firebase_credentials_temp.json")
