import streamlit as st

from db import SessionLocal
from repositories import receipt
from services.scanner import parse_receipt_text

st.title("📷 Food Online Receipt")

# File uploader
uploaded_file = st.file_uploader(
    "Choose an image...", type=["jpg", "jpeg", "png"]
)

# API endpoint (replace with your real API)
API_URL = "http://localhost:8000/upload"

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

    if st.button("Save to DB"):
        # Prepare the file for sending
        files = {
            "file": (uploaded_file.name, uploaded_file, uploaded_file.type)
        }
        payload = parse_receipt_text(uploaded_file.read())
        st.write(payload)
        with SessionLocal() as session:
            receipt.add(session, payload)
