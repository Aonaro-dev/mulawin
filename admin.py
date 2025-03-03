import streamlit as st
from firebase_admin import db

# Firebase Database reference for user data
ref = db.reference("/users")

def admin_page():
    st.title("Admin Page")

    # Fetch all users from Firebase
    users = ref.get()

    if users:
        for user_id, user_data in users.items():
            email = user_data.get("email")
            approved = user_data.get("approved")

            col1, col2 = st.columns([3, 1])
            col1.write(email)
            if approved:
                col2.success("Approved")
            else:
                if col2.button("Approve", key=user_id):
                    # Update approval status in the database
                    ref.child(user_id).update({"approved": True})
                    st.experimental_rerun()
    else:
        st.write("No users to approve.")

# Show admin page
admin_page()
