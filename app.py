
import streamlit as st
import requests
import hashlib

# -------------------- PAGE CONFIG --------------------

st.set_page_config(
    page_title="OrgBot | Organisation AI Assistant",
    page_icon="🤖",
    layout="wide"
)

BASE_URL = "http://127.0.0.1:8000"
ASK_URL = f"{BASE_URL}/ask"
UPLOAD_URL = f"{BASE_URL}/upload"
HEALTH_URL = f"{BASE_URL}/health"


# -------------------- CUSTOM DESIGN --------------------

st.markdown("""
<style>
    .stApp {
        background-color: #0b1120;
        color: #f1f5f9;
    }

    [data-testid="stSidebar"] {
        background-color: #111c31;
        border-right: 1px solid #263650;
    }

    .hero {
        padding: 28px;
        border-radius: 18px;
        background: linear-gradient(120deg, #172554, #123b59);
        border: 1px solid #29476b;
        margin-bottom: 22px;
    }

    .hero h1 {
        color: #ffffff;
        font-size: 38px;
        margin-bottom: 8px;
    }

    .hero p {
        color: #cbd5e1;
        font-size: 16px;
        margin-bottom: 0;
    }

    .info-card {
        background: #142137;
        border: 1px solid #263650;
        border-radius: 14px;
        padding: 18px;
        min-height: 105px;
    }

    .info-card h3 {
        color: #e2e8f0;
        margin: 0 0 7px 0;
        font-size: 17px;
    }

    .info-card p {
        color: #94a3b8;
        margin: 0;
        font-size: 13px;
    }

    .section-heading {
        color: #e2e8f0;
        font-size: 22px;
        font-weight: 650;
        margin-top: 22px;
        margin-bottom: 10px;
    }

    .small-note {
        color: #94a3b8;
        font-size: 13px;
    }

    [data-testid="stChatMessage"] {
        border: 1px solid #263650;
        border-radius: 14px;
        padding: 12px;
    }

    .stChatInput textarea {
        background-color: #142137;
    }
</style>
""", unsafe_allow_html=True)


# -------------------- SESSION STATE --------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_documents" not in st.session_state:
    st.session_state.uploaded_documents = []

if "uploaded_signatures" not in st.session_state:
    st.session_state.uploaded_signatures = set()


# -------------------- SIDEBAR --------------------

with st.sidebar:

    st.markdown("## 🤖 OrgBot")
    st.caption("Organisation Knowledge Assistant")

    st.divider()

    st.markdown("### 📁 Knowledge Base")

    st.write(
        "Upload organisation documents to make them searchable."
    )

    # Select PDF
    uploaded_file = st.file_uploader(
        "Choose a PDF document",
        type=["pdf"],
        help="Upload notices, brochures, policies, fee structures or other organisation PDFs.",
        key="orgbot_pdf_uploader"
    )

    # Automatically upload when a new PDF is selected
    if uploaded_file is not None:

        file_bytes = uploaded_file.getvalue()

        # Unique signature based on filename and file content
        file_signature = hashlib.sha256(
            uploaded_file.name.encode("utf-8") + file_bytes
        ).hexdigest()

        if file_signature not in st.session_state.uploaded_signatures:

            try:
                with st.spinner("OrgBot is processing your PDF..."):

                    files = {
                        "file": (
                            uploaded_file.name,
                            file_bytes,
                            "application/pdf"
                        )
                    }

                    response = requests.post(
                        UPLOAD_URL,
                        files=files,
                        timeout=240
                    )

                    response.raise_for_status()

                    result = response.json()

                # Mark as uploaded only after successful processing
                st.session_state.uploaded_signatures.add(
                    file_signature
                )

                if uploaded_file.name not in st.session_state.uploaded_documents:
                    st.session_state.uploaded_documents.append(
                        uploaded_file.name
                    )

                st.success("PDF uploaded and processed successfully!")

                st.write(
                    "**Document:**",
                    result.get("filename", uploaded_file.name)
                )

                st.write(
                    "**Pages processed:**",
                    result.get("pages_processed", "N/A")
                )

                st.write(
                    "**Chunks created:**",
                    result.get("chunks_created", "N/A")
                )

            except requests.exceptions.Timeout:
                st.error("PDF upload timed out. Please try again.")

            except requests.exceptions.HTTPError as error:
                st.error("Backend rejected the PDF upload.")
                st.code(str(error))

                if response is not None:
                    st.code(response.text)

            except requests.exceptions.RequestException as error:
                st.error("Could not connect to OrgBot backend.")
                st.code(str(error))

            except ValueError:
                st.error("Invalid response received from backend.")

    st.divider()

    # Uploaded document list
    st.markdown("### 📚 Uploaded This Session")

    if st.session_state.uploaded_documents:

        for document in st.session_state.uploaded_documents:
            st.markdown(f"📄 {document}")

    else:
        st.caption("No documents uploaded in this session yet.")

    st.divider()

    # Clear chat
    if st.button("🗑️ Clear Chat", use_container_width=True):

        st.session_state.messages = []
        st.rerun()

    st.caption("OrgBot | Document-grounded AI assistant")


# -------------------- MAIN HEADER --------------------

st.markdown("""
<div class="hero">
    <h1>🤖 OrgBot</h1>
    <p>Your organisation's information, available through one intelligent assistant.</p>
</div>
""", unsafe_allow_html=True)


# -------------------- BACKEND STATUS --------------------

backend_online = False

try:
    health_response = requests.get(
        HEALTH_URL,
        timeout=5
    )

    backend_online = health_response.status_code == 200

except requests.exceptions.RequestException:
    backend_online = False


col1, col2, col3 = st.columns(3)

with col1:

    st.markdown("""
    <div class="info-card">
        <h3>📄 Document Intelligence</h3>
        <p>Upload and search organisation PDFs.</p>
    </div>
    """, unsafe_allow_html=True)


with col2:

    st.markdown("""
    <div class="info-card">
        <h3>💬 AI Conversations</h3>
        <p>Ask questions in natural language.</p>
    </div>
    """, unsafe_allow_html=True)


with col3:

    status_text = (
        "Backend Connected"
        if backend_online
        else "Backend Offline"
    )

    status_icon = "🟢" if backend_online else "🔴"

    st.markdown(f"""
    <div class="info-card">
        <h3>{status_icon} {status_text}</h3>
        <p>Connection to the OrgBot API.</p>
    </div>
    """, unsafe_allow_html=True)


# -------------------- CHAT SECTION --------------------

st.markdown(
    '<div class="section-heading">💬 Ask OrgBot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="small-note">Ask about notices, deadlines, fees, timings, policies and other uploaded information.</p>',
    unsafe_allow_html=True
)


# -------------------- DISPLAY CHAT HISTORY --------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant" and message.get("sources"):

            with st.expander("📚 View Sources"):

                for source in message["sources"]:

                    st.write(
                        f"📄 {source.get('file', 'Document')} "
                        f"— Page {source.get('page', 'N/A')}"
                    )


# -------------------- CHAT INPUT --------------------

question = st.chat_input(
    "Ask something about your organisation..."
)


if question:

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        if not backend_online:

            answer = (
                "I cannot connect to the OrgBot backend. "
                "Please start the FastAPI server and try again."
            )

            sources = []

            st.error(answer)

        else:

            with st.spinner("OrgBot is searching your documents..."):

                try:

                    response = requests.post(
                        ASK_URL,
                        json={"question": question},
                        timeout=240
                    )

                    response.raise_for_status()

                    result = response.json()

                    answer = result.get(
                        "answer",
                        "Sorry, I could not generate an answer."
                    )

                    sources = result.get("sources", [])

                    st.markdown(answer)

                    if sources:

                        with st.expander("📚 View Sources"):

                            for source in sources:

                                st.write(
                                    f"📄 {source.get('file', 'Document')} "
                                    f"— Page {source.get('page', 'N/A')}"
                                )

                except requests.exceptions.Timeout:

                    answer = (
                        "The request took too long. "
                        "Please try again in a moment."
                    )

                    sources = []

                    st.error(answer)

                except requests.exceptions.RequestException as error:

                    answer = (
                        "Something went wrong while contacting OrgBot. "
                        "Please check the backend."
                    )

                    sources = []

                    st.error(answer)

                    st.caption(str(error))

                except ValueError:

                    answer = "The backend returned an invalid response."

                    sources = []

                    st.error(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources
    })
