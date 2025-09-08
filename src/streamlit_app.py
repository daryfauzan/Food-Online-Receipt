import streamlit as st
from dotenv import load_dotenv

from db import engine
from models import Base

Base.metadata.create_all(engine)

load_dotenv("../.env")

upload_page = st.Page(
    "pages/upload_receipt.py", title="Upload Receipt", icon="📷"
)
chat_page = st.Page("pages/chat.py", title="Ask AI", icon="💬")


pg = st.navigation([upload_page, chat_page])
pg.run()
