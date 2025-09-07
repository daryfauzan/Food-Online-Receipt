import streamlit as st

from src.db import Base, engine

Base.metadata.create_all(engine)

home_page = st.Page("pages/home.py", title="Home", icon="🏠")
upload_page = st.Page(
    "pages/upload_receipt.py", title="Upload Receipt", icon="📷"
)
chat_page = st.Page("pages/chat.py", title="Ask AI", icon="💬")


pg = st.navigation([home_page, upload_page, chat_page])
pg.run()
