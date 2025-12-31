import uuid
import streamlit as st

from src.agent.agno_agent import ChaanakyaAgent


def render_sidebar():
    with st.sidebar:
        st.title("🧠 The Chaanakya")

        # -------------------------
        # Init rename state
        # -------------------------
        if "renaming_chat_id" not in st.session_state:
            st.session_state.renaming_chat_id = None

        # -------------------------
        # New Chat Button
        # -------------------------
        if st.button("➕ New Chat", use_container_width=True):
            chat_id = str(uuid.uuid4())
            st.session_state.chats[chat_id] = {
                "name": "New Legal Chat",
                "agent": ChaanakyaAgent(session_id=chat_id),
            }
            st.session_state.active_chat_id = chat_id
            st.session_state.renaming_chat_id = None
            st.rerun()

        st.divider()

        # -------------------------
        # Chat List
        # -------------------------
        for chat_id, chat_data in st.session_state.chats.items():
            is_active = chat_id == st.session_state.active_chat_id
            is_renaming = chat_id == st.session_state.renaming_chat_id

            col1, col2 = st.columns([0.8, 0.2])

            # -------------------------
            # Rename Mode
            # -------------------------
            if is_renaming:
                new_name = st.text_input(
                    "Rename chat",
                    value=chat_data["name"],
                    key=f"rename_input_{chat_id}",
                )

                if st.button("✅ Save", key=f"save_{chat_id}"):
                    if new_name.strip():
                        st.session_state.chats[chat_id]["name"] = new_name.strip()
                    st.session_state.renaming_chat_id = None
                    st.rerun()

            # -------------------------
            # Normal Mode
            # -------------------------
            else:
                if col1.button(
                    chat_data["name"],
                    key=f"select_{chat_id}",
                    use_container_width=True,
                    type="primary" if is_active else "secondary",
                ):
                    st.session_state.active_chat_id = chat_id
                    st.session_state.renaming_chat_id = None
                    st.rerun()

                if col2.button("✏️", key=f"edit_{chat_id}"):
                    st.session_state.renaming_chat_id = chat_id
                    st.rerun()
