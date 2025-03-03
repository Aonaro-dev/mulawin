import streamlit as st
from firebase_admin import firestore
import firebase_admin

# Initialize Firestore
db = firestore.client()

# Firebase Auth
auth_client = firebase_admin.auth

def admin_page():
    st.title("Admin Page")

    # Get current logged-in user (replace this with your actual login check)
    user_id = st.experimental_get_query_params().get('user_id', [None])[0]
    if not user_id:
        st.error("You must be logged in.")
        return

    # Fetch the current user from Firestore
    user_doc = db.collection("users").document(user_id).get()
    user_data = user_doc.to_dict()

    # Check if the user is an admin
    if user_data.get("role") != "admin":
        st.error("You do not have permission to view this page.")
        return

    st.write("Welcome Admin!")

    # Fetch all users from Firestore
    users_ref = db.collection("users")
    users = users_ref.stream()

    for user in users:
        user_data = user.to_dict()
        email = user_data.get("email")
        approved = user_data.get("approved")

        col1, col2 = st.columns([3, 1])
        col1.write(email)
        if approved:
            col2.success("Approved")
        else:
            if col2.button("Approve", key=user.id):
                # Update approval status in Firestore
                users_ref.document(user.id).update({"approved": True})
                st.experimental_rerun()

# Show admin page
admin_page()
