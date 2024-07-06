import streamlit as st
import requests
import base64

def convert_image_to_base64(image):
    return base64.b64encode(image.read()).decode('utf-8')

st.title("Smart Meter Image Processing")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)

    # Convert the uploaded image to base64
    base64_image = convert_image_to_base64(uploaded_file)

    # Define the API endpoint and headers
    url = "http://127.0.1:8000/Smart_Meter/"
    api_key = "apikey1"  # Replace with the appropriate API key
    headers = {
        "Content-Type": "application/json",
        "api_key": api_key
    }
    data = {
        "image_data": base64_image
    }

    # Send the image to the FastAPI endpoint
    if st.button("Process Image"):
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            st.write(result)
            if 'outputImage' in result['data']:
                output_image_data = base64.b64decode(result['data']['outputImage'])
                st.image(output_image_data, caption='Processed Image', use_column_width=True)
            if 'meterNumber' in result['data']:
                st.write(f"Meter Number: {result['data']['meterNumber']}")
        else:
            st.write("Error in processing the image")
