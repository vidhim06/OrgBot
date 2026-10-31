
import streamlit as st
import requests

# Page configuration
st.set_page_config(
    page_title="OrgBot - AI Assistant",
    page_icon="🤖",
    layout="centered"
)

# Application title
st.title("🤖 OrgBot")
st.caption("Your AI assistant for organisation documents")

st.divider()

# Backend API URL
API_URL = "http://127.0.0.1:8000/ask"

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
question = st.chat_input("Ask something about your documents...")

if question:
    # Display user question
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.write(question)

    # Get answer from FastAPI
    with st.chat_message("assistant"):
        with st.spinner("OrgBot is thinking..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"question": question},
                    timeout=60
                )

                response.raise_for_status()
                result = response.json()

                answer = result.get(
                    "answer",
                    "Sorry, no answer was generated."
                )

                st.write(answer)

                # Display sources
                sources = result.get("sources", [])

                if sources:
                    with st.expander("View Sources"):
                        for source in sources:
                            st.write(
                                f"📄 {source['file']} "
                                f"— Page {source['page']}"
                            )

            except requests.exceptions.RequestException as error:
                answer = "Unable to connect to OrgBot backend. Please check whether the API server is running."
                st.error(answer)
                st.caption(str(error))

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
