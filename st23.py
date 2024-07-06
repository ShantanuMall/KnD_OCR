import streamlit as st
import os
import datetime
import base64
from main import pipeline

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        base64_encoded = base64.b64encode(image_file.read()).decode("utf-8")
    return base64_encoded

def process_image(image_data):
    try:
        # Decode base64 image data
        image_content = base64.b64decode(image_data)
        image_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

        # Save the decoded image in the uploads folder
        image_path = os.path.join(upload_dir, f"{image_name}.jpeg")
        with open(image_path, "wb") as temp_image_file:
            temp_image_file.write(image_content)

        try:
            status, message, result, path = pipeline(source=image_path)
            from pathlib import Path
            if Path(path).exists():
                img64 = image_to_base64(path)
            else:
                img64 = path
        except Exception as e:
            return {"error": f"OCR error: {str(e)}"}

        try:
            os.remove(image_path)
        except Exception as e:
            return {"error": f"File delete error: {str(e)}"}

        response = {
            "status": status,
            "message": message,
            "data": {
                "outputImage": img64,
                "meterNumber": result
            }
        }
        return response
    except Exception as e:
        return {"error": str(e)}

# Define a directory to store uploaded images
upload_dir = "uploads"
os.makedirs(upload_dir, exist_ok=True)

st.title("KnD: Smart Meter OCR App")

# File uploader for image upload
uploaded_file = st.file_uploader("Upload a photo of your smart meter", type=["jpeg", "jpg", "png"])

if uploaded_file is not None:
    # Convert the uploaded file to base64
    image_bytes = uploaded_file.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    # Process the image
    with st.spinner("Processing image..."):
        result = process_image(image_base64)
    
    # Display the results
    if "error" in result:
        st.error(result["error"])
    else:
        st.success(result["message"])
        st.image(base64.b64decode(result["data"]["outputImage"]), caption="Processed Image")
        st.write("Meter Reading: ", result["data"]["meterNumber"])
