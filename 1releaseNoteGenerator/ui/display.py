import streamlit as st
import requests

# Set the FastAPI backend URL
FASTAPI_URL = "http://127.0.0.1:8000/create-release-notes"

# Streamlit UI
st.title("Release Note Creator")

# Input fields
token = st.text_input("Enter GitLab Token", placeholder="glpat-xyxyxyxyxy")
url = st.text_input("Enter GitLab URL", placeholder="gitlab.com")
project_id = st.text_input("Enter Project ID", placeholder="123456")

# Submit button
if st.button("Submit"):
    
    errors = []

    # Validate token
    if not token:
        errors.append("Token is required.")
    
    # Validate URL
    if not url:
        errors.append("URL is required.")

    # Validate age
    if not project_id:
        errors.append("Project ID is required.")
    try:
        id = int(project_id)
        if id <= 0:
            errors.append("Project ID must be a positive number.")
    except ValueError:
        errors.append("Project ID must be a number.")

    # Display errors or success message
    if errors:
        for error in errors:
            st.error(error)
    else:
        # Prepare data for FastAPI
        input_data = {
            "access_token": token,
            "base_url": url,
            "project_id": project_id,
        }
        # Send POST request to FastAPI
        try:
            response = requests.post(FASTAPI_URL, json=input_data)
            response.raise_for_status()  # Raise error for non-200 responses
            result = response.json()
            st.success(f"Response: \n {result['message']}")
            # st.success({result['message']})
        except requests.exceptions.RequestException as e:
            st.error(f"Error: {e}")
