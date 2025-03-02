import streamlit as st
from firebase_admin import credentials, firestore
import json

# Use credentials from secrets
firebase_credentials = st.secrets["firebase"]
cred = credentials.Certificate(json.loads(firebase_credentials))
firebase_admin.initialize_app(cred)

db = firestore.client()

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
