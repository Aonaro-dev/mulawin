import streamlit as st
from auth import Authenticator

# Retrieve secrets from Streamlit's secrets management
allowed_users = st.secrets["ALLOWED_USERS"].split(",")
token_key = st.secrets["TOKEN_KEY"]
client_secret = st.secrets["client_secret"]
redirect_uri = st.secrets["REDIRECT_URI"]

st.title("Streamlit Google Auth")

# Write the client secret json data into a temporary file
with open("client_secret_temp.json", "w") as secret_file:
    secret_file.write(client_secret)

authenticator = Authenticator(
    allowed_users=allowed_users,
    token_key=token_key,
    secret_path="client_secret_temp.json",  # Use the temp file with client secrets
    redirect_uri=redirect_uri,
)
authenticator.check_auth()
authenticator.login()

# Show content that requires login
if st.session_state["connected"]:
    st.write(f"welcome! {st.session_state['user_info'].get('email')}")
    if st.button("Log out"):
        authenticator.logout()

if not st.session_state["connected"]:
    st.write("you have to log in first ...")
