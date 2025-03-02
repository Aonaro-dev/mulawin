import streamlit as st
from authlib.integrations.requests_client import OAuth2Session

# App title
st.title("Streamlit App with Google Login")

# Google OAuth credentials from Streamlit secrets
client_id = st.secrets["oauth"]["client_id"]
client_secret = st.secrets["oauth"]["client_secret"]
redirect_uri = st.secrets["oauth"]["redirect_uri"]

# Initialize OAuth 2.0 session
oauth = OAuth2Session(client_id, client_secret, redirect_uri=redirect_uri)

# Authorization URL
authorization_url, state = oauth.create_authorization_url(
    "https://accounts.google.com/o/oauth2/auth",
    scope=["openid", "email", "profile"],
    prompt="select_account"
)

# Display the login button
if 'userinfo' not in st.session_state:
    st.write("Please log in to continue:")
    if st.button("Login with Google"):
        st.write("Redirecting to Google login...")
        st.markdown(f"[Login with Google]({authorization_url})")

# Handle the OAuth callback (when the user is redirected back to the app after login)
if 'code' in st.experimental_get_query_params():
    code = st.experimental_get_query_params()['code'][0]
    
    # Exchange the authorization code for an access token
    token = oauth.fetch_token(
        "https://oauth2.googleapis.com/token",
        authorization_response=f"{redirect_uri}?code={code}",
        client_secret=client_secret,
    )
    
    # Fetch user profile information from Google
    userinfo = oauth.get("https://www.googleapis.com/oauth2/v3/userinfo").json()

    # Store user info in session state
    st.session_state['userinfo'] = userinfo

    # Display user info
    st.success(f"Logged in as {userinfo['name']}")
    st.image(userinfo['picture'], width=100)
    
# Display the app content only if the user is logged in
if 'userinfo' in st.session_state:
    st.write(f"Welcome, {st.session_state['userinfo']['name']}! Here's the main content of the app:")
    
    # Main content of your app goes here
    st.write("This is your app's main interface, accessible only to logged-in users.")
    
    # Add any additional app logic here
    st.write("You can now show your app's functionality!")

else:
    st.warning("Please log in to access the app.")
