import streamlit as st
from firebase_admin import firestore

# Ensure user is logged in
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in to access the admin page.")
    st.stop()

# Check if the user is admin
if st.session_state.role != "admin":
    st.error("Unauthorized access. Only admins can access this page.")
    st.stop()

# Firestore client
db = firestore.client()

def admin_page():
    st.title("Admin Page")
    st.write("Welcome, Admin! Manage user approvals here.")

    # List all unapproved users
    users = db.collection("users").where("approved", "==", False).stream()

    for user in users:
        user_data = user.to_dict()
        st.write(f"Email: {user_data['email']}")
        if st.button(f"Approve {user_data['email']}"):
            db.collection("users").document(user.id).update({"approved": True})
            st.success(f"User {user_data['email']} approved!")

admin_page()
