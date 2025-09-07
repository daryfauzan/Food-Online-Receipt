import requests
import streamlit as st

st.title("📷 Food Online Receipt")

# File uploader
uploaded_file = st.file_uploader(
    "Choose an image...", type=["jpg", "jpeg", "png"]
)

# API endpoint (replace with your real API)
API_URL = "http://localhost:8000/upload"

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

    if st.button("Send to API"):
        # Prepare the file for sending
        files = {
            "file": (uploaded_file.name, uploaded_file, uploaded_file.type)
        }

        try:
            response = requests.post(API_URL, files=files)
            if response.status_code == 200:
                st.success("✅ Image sent successfully!")
                st.json(response.json())
            else:
                st.error(
                    f"❌ Failed to send image. Status: {response.status_code}"
                )
                st.text(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
