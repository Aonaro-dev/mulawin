import streamlit as st
from authlib.integrations.requests_client import OAuth2Session
import firebase_admin
from firebase_admin import credentials, auth

# Firebase credentials (make sure this is set up correctly)
firebase_credentials = dict(st.secrets["firebase"])

# Initialize Firebase Admin if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_credentials)
    firebase_admin.initialize_app(cred)

# Google OAuth Configurations
client_id = st.secrets["google_oauth"]["client_id"]
client_secret = st.secrets["google_oauth"]["client_secret"]
redirect_uri = st.secrets["firebase"]["redURL"]  # Your streamlit app's address

oauth = OAuth2Session(client_id, client_secret, redirect_uri=redirect_uri)

authorization_endpoint = 'https://accounts.google.com/o/oauth2/auth'
token_endpoint = 'https://oauth2.googleapis.com/token'

# Step 1: User clicks login button
if st.button('Login with Google'):
    # Redirect the user to the Google login page
    uri, state = oauth.create_authorization_url(authorization_endpoint, 
                                                scope=["openid", "email", "profile"])
    st.experimental_set_query_params(state=state)
    st.write(f"Go to the following URL to login: {uri}")

# Step 2: After the user logs in and Google redirects back
query_params = st.experimental_get_query_params()
code = query_params.get('code')

if code:
    token = oauth.fetch_token(token_endpoint, code=code, authorization_response=st.request.url)
    user_info = oauth.get('https://www.googleapis.com/oauth2/v1/userinfo').json()

    st.write(f"Logged in as {user_info['email']}")

    # Verify token with Firebase Admin
    try:
        decoded_token = auth.verify_id_token(token['id_token'])
        st.write(f"Firebase User ID: {decoded_token['uid']}")
    except Exception as e:
        st.error(f"Token verification failed: {e}")
