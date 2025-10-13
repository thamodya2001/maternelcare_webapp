import re
import streamlit as st
import requests
import time

WEBHOOK_URL = st.secrets['WEBHOOK_URL']

def is_valid_email(email):
    # Improved email validation regex
    email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_pattern, email) is not None

def contact_form():
    with st.form("contact_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        message = st.text_area("Your Message")
        submit_button = st.form_submit_button("Submit")

    if submit_button:
        # Validation checks
        if not name:
            st.error("Please provide your name.", icon="🧑")
            return

        if not email:
            st.error("Please provide your email address.", icon="📨")
            return

        if not is_valid_email(email):
            st.error("Please provide a valid email address.", icon="📧")
            return

        if not message:
            st.error("Please provide a message.", icon="💬")
            return

        # Show loading indicator
        with st.spinner("Sending your message..."):
            try:
                # Prepare the data payload
                data = {
                    "email": email, 
                    "name": name, 
                    "message": message,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                
                # Debug information
                #st.write("📤 Sending data to webhook...")
                
                # Send the request with timeout
                response = requests.post(
                    WEBHOOK_URL, 
                    json=data, 
                    timeout=10,
                    headers={
                        "Content-Type": "application/json",
                        "User-Agent": "Streamlit-App/1.0"
                    }
                )
                
                # Debug response
                #st.write(f"📡 Response Status Code: {response.status_code}")
                
                if response.status_code == 200:
                    st.success("Your message has been sent successfully! 🎉")
                    #st.balloons()
                else:
                    st.error(f"Failed to send message. Server returned status: {response.status_code}")
                    st.write(f"Response text: {response.text}")
                    
            except requests.exceptions.Timeout:
                st.error("Request timed out. Please try again.", icon="⏰")
            except requests.exceptions.ConnectionError:
                st.error("Connection error. Please check your internet connection.", icon="🌐")
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred: {str(e)}", icon="❌")
            except Exception as e:
                st.error(f"Unexpected error: {str(e)}", icon="💥")

# Usage in your Streamlit app
st.title("Contact Us")
contact_form()