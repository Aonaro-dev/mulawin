import streamlit as st
from requests_oauthlib import OAuth2Session
import os

# Retrieve Google OAuth credentials from Streamlit secrets
GOOGLE_CLIENT_ID = st.secrets["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = st.secrets["GOOGLE_CLIENT_SECRET"]
REDIRECT_URI = st.secrets["REDIRECT_URI"]

AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"

# OAuth2Session object for login
def create_oauth_session():
    return OAuth2Session(
        GOOGLE_CLIENT_ID,
        redirect_uri=REDIRECT_URI,
        scope=["openid", "email", "profile"]
    )

# Google Login Page
def login():
    if "token" not in st.session_state:
        oauth = create_oauth_session()
        authorization_url, state = oauth.authorization_url(AUTHORIZATION_URL)
        st.write(f"[Login with Google]({authorization_url})")

    else:
        st.write("Logged in successfully!")

if __name__ == "__main__":
    st.title("Login with Google")
    login()
