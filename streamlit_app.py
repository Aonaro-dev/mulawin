import streamlit as st
from firebase_admin import credentials, firestore

# Use credentials from secrets directly (no need for json.loads)
firebase_credentials = st.secrets["firebase"]
cred = credentials.Certificate(firebase_credentials)  # No json.loads here
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
