# OrgBot – AI Assistant for Any Organisation

OrgBot is a multi-tenant AI-powered chatbot that helps organisations provide instant answers to questions using their uploaded PDF documents.

It uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant information from organisation-specific documents and generate context-aware answers with source references.

## Features

- **User Authentication:** Secure registration and login.
- **Multi-Tenant Architecture:** Keeps document retrieval separated by organisation.
- **PDF Upload:** Upload organisational documents through the dashboard.
- **AI-Powered Q&A:** Ask questions in natural language and receive answers based on uploaded documents.
- **Source References:** Displays the source document and page number for answers.
- **Interactive Dashboard:** Manage documents and access the chatbot through a React interface.
- **Persistent Storage:** Stores document metadata in MySQL and document embeddings in ChromaDB.

## Tech Stack

| Component | Technologies |
|---|---|
| Frontend | React.js, Vite, CSS |
| Backend | Python, FastAPI |
| Database | MySQL, SQLAlchemy |
| Vector Database | ChromaDB |
| AI / LLM | Google Gemini API |
| Embeddings | Sentence Transformers |
| Document Processing | PDF processing, text chunking |
| Authentication | JWT, Password Hashing |
| Tools | Git, GitHub, VS Code |

## System Architecture

1. Users register or log in to their organisation workspace.
2. Users upload PDF documents through the React dashboard.
3. FastAPI processes the uploaded documents and extracts their text.
4. Extracted text is divided into smaller chunks.
5. Sentence Transformers generate embeddings for the chunks.
6. ChromaDB stores the embeddings with organisation-specific metadata.
7. When a user asks a question, OrgBot generates a query embedding and retrieves relevant chunks belonging to that organisation.
8. Google Gemini generates an answer using the retrieved context.
9. The chatbot displays the answer along with source document references.

## Project Structure

```text
OrgBot/
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   ├── App.jsx
│   │   └── App.css
│   ├── package.json
│   └── index.html
│
├── src/
│   ├── api/
│   ├── auth/
│   ├── database/
│   ├── document_processing/
│   ├── generation/
│   └── ...
│
├── data/
├── tests/
├── requirements.txt
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.12
- Node.js and npm
- MySQL
- Google Gemini API key

### 1. Clone the Repository

```bash
git clone https://github.com/vidhim06/OrgBot.git
cd OrgBot
```

### 2. Backend Setup

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
DATABASE_URL=mysql+pymysql://username:password@localhost/orgbot_saas
```

Replace the placeholder values with your own credentials.

### 4. Start the Backend

```bash
python -m uvicorn src.api.main:app --reload
```

Backend: `http://127.0.0.1:8000`

API documentation: `http://127.0.0.1:8000/docs`

### 5. Frontend Setup

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend: `http://localhost:5173`

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Authenticate a user |
| GET | `/auth/me` | Get logged-in user details |
| POST | `/upload` | Upload a PDF document |
| GET | `/documents` | Retrieve organisation documents |
| POST | `/ask` | Ask questions about uploaded documents |
| GET | `/health` | Check backend health |

## Future Improvements

- Persistent chatbot configuration.
- Document deletion and management.
- Public chatbot sharing.
- Analytics and usage tracking.
- Improved multilingual support.
- Deployment and production-ready infrastructure.

## Author

**Vidhi Mittal**

B.Tech – Computer Science and Engineering (Data Science)

- GitHub: [vidhim06](https://github.com/vidhim06)

---

*OrgBot – Making organisational information easier to access through AI.*