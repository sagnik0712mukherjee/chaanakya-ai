import uuid
import streamlit as st

from src.agent.agno_agent import ChaanakyaAgent
from src.ui_pages.sidebar import render_sidebar
from src.ui_pages.chat import render_chat


st.set_page_config(
    page_title="💡 The Chaanakya — Your Legal AI Assistant",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------
# Legal Font
# -------------------------
st.markdown(
    """
    <style>

    /* ===== OPTION 1: Playfair Display (Royal / Courtroom) ===== */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&display=swap');
    * {
        font-family: 'Playfair Display', Georgia, serif !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# -------------------------
# Session State Init
# -------------------------

if "chats" not in st.session_state:
    chat_id = str(uuid.uuid4())
    st.session_state.chats = {
        chat_id: {
            "name": "New Legal Chat",
            "agent": ChaanakyaAgent(session_id=chat_id),
        }
    }
    st.session_state.active_chat_id = chat_id


# -------------------------
# Sidebar
# -------------------------

render_sidebar()


# -------------------------
# Main Chat Area
# -------------------------

active_chat = st.session_state.chats[st.session_state.active_chat_id]
render_chat(active_chat)
