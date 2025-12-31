import streamlit as st


def render_chat(chat_data):
    agent = chat_data["agent"]

    st.header(chat_data["name"])

    # -------------------------
    # Render Conversation
    # -------------------------
    for msg in agent.get_conversation():
        role = msg.get("role", "assistant")
        content = msg.get("content", "")

        with st.chat_message(role):
            st.markdown(content)

    # -------------------------
    # User Input
    # -------------------------
    user_input = st.chat_input("Ask a legal question...")

    if user_input:
        # Show user message
        with st.chat_message("user"):
            st.markdown(user_input)

        # Run agent
        with st.chat_message("assistant"):
            with st.spinner("Chaanakya is thinking..."):
                response = agent.run(user_input)
                st.markdown(response)

        st.rerun()
