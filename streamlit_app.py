import streamlit as st
from requests_oauthlib import OAuth2Session
import os

# Google OAuth 2.0 Credentials from Streamlit secrets
GOOGLE_CLIENT_ID = st.secrets["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = st.secrets["GOOGLE_CLIENT_SECRET"]
REDIRECT_URI = st.secrets["REDIRECT_URI"]

# Google OAuth Endpoints
AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"

# OAuth2Session object to manage login
def create_oauth_session(state=None):
    return OAuth2Session(
        GOOGLE_CLIENT_ID,
        redirect_uri=REDIRECT_URI,
        scope=["openid", "email", "profile"],
        state=state
    )

def login():
    if "token" not in st.session_state:
        # If no token, start the login process
        oauth = create_oauth_session()
        authorization_url, state = oauth.authorization_url(AUTHORIZATION_URL)

        # Save state in session to validate later
        st.session_state["oauth_state"] = state

        # Provide login link to user
        st.write(f"[Login with Google]({authorization_url})")

    else:
        st.write("Logged in successfully!")
        token = st.session_state["token"]
        st.write(f"Access Token: {token}")

def handle_callback():
    # Handle the callback from Google
    if st.experimental_get_query_params().get("code"):
        oauth = create_oauth_session(state=st.session_state["oauth_state"])
        token = oauth.fetch_token(
            TOKEN_URL,
            client_secret=GOOGLE_CLIENT_SECRET,
            authorization_response=st.experimental_get_query_params()["code"][0],
        )
        st.session_state["token"] = token

def main():
    st.title("Login with Google")

    # Handle OAuth callback when redirected back
    query_params = st.experimental_get_query_params()
    if "code" in query_params:
        handle_callback()

    if "token" in st.session_state:
        st.write("You are already logged in.")
    else:
        login()

if __name__ == "__main__":
    main()
