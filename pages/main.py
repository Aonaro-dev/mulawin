import streamlit as st

# Ensure user is logged in
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in to access the main page.")
    st.stop()

# Main page content
st.title("Main Page")
st.write("Welcome to the main page!")
