
from pathlib import Path
from uuid import uuid4
from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException,
    Depends
)

from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel
from src.auth.dependencies import get_current_user
from src.database.models import User, Document
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.document_processing.pdf_reader import extract_pages_from_pdf
from src.document_processing.text_chunker import chunk_pages
from src.document_processing.embedding_model import generate_embeddings
from src.document_processing.vector_store import VectorStore
from src.generation.qa_pipeline import answer_question
import time
from src.auth.routes import router as auth_router
app = FastAPI(title="OrgBot API")
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)

UPLOAD_DIR = Path("data/uploads")
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "Welcome to OrgBot!"}


@app.get("/health")
def health():
    return {"status": "healthy"}



@app.post("/ask")
async def ask_question(
    request: QuestionRequest,
    current_user: User = Depends(get_current_user),
):
    try:
        result = answer_question(
            request.question,
            organisation_id=current_user.organisation_id
        )
        return result

    except Exception as error:
        import traceback
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=f"Question processing failed: {str(error)}"
        )


@app.get("/documents")
async def get_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    documents = (
        db.query(Document)
        .filter(
            Document.organisation_id == current_user.organisation_id
        )
        .order_by(Document.created_at.desc())
        .all()
    )

    return {
        "documents": [
            {
                "id": document.id,
                "filename": document.filename,
                "pages_processed": document.pages_processed,
                "chunks_created": document.chunks_created,
                "status": document.status,
                "created_at": document.created_at.isoformat()
                if document.created_at else None
            }
            for document in documents
        ]
    }



@app.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    total_start = time.perf_counter()
    stored_path = None

    try:
        if not file.filename or Path(file.filename).suffix.lower() != ".pdf":
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed."
            )

        content = await file.read()

        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="File size must not exceed 20 MB."
            )

        if not content.startswith(b"%PDF"):
            raise HTTPException(
                status_code=400,
                detail="Invalid PDF file."
            )

        original_filename = Path(file.filename).name
        organisation_id = current_user.organisation_id

        # Create a separate upload folder for each organisation
        organisation_upload_dir = UPLOAD_DIR / str(organisation_id)
        organisation_upload_dir.mkdir(parents=True, exist_ok=True)

        stored_path = organisation_upload_dir / f"{uuid4().hex}.pdf"
        stored_path.write_bytes(content)

        # Extract PDF text
        pages = extract_pages_from_pdf(str(stored_path))

        if not pages:
            raise HTTPException(
                status_code=400,
                detail="No readable text found in this PDF."
            )

        for page in pages:
            page["source"] = original_filename

        # Create chunks
        chunks = chunk_pages(pages)

        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="No text chunks could be created."
            )

        # Generate embeddings
        embeddings = generate_embeddings(
            [chunk["text"] for chunk in chunks]
        )

        # Store chunks for this organisation
        store = VectorStore()
        store.add_chunks(
            chunks,
            embeddings,
            organisation_id=organisation_id
        )

        # Save document details in MySQL
        document = Document(
            filename=original_filename,
            file_path=str(stored_path),
            pages_processed=len(pages),
            chunks_created=len(chunks),
            status="Processed",
            organisation_id=organisation_id
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        print(
            f"TOTAL UPLOAD TIME: "
            f"{time.perf_counter() - total_start:.2f}s"
        )

        return {
            "message": "PDF uploaded and processed successfully!",
            "document_id": document.id,
            "filename": original_filename,
            "pages_processed": len(pages),
            "chunks_created": len(chunks),
            "organisation_id": organisation_id
        }

    except HTTPException:
        if stored_path:
            stored_path.unlink(missing_ok=True)
        raise

    except Exception as error:
        db.rollback()

        if stored_path:
            stored_path.unlink(missing_ok=True)

        raise HTTPException(
            status_code=500,
            detail=f"PDF processing failed: {str(error)}"
        )

    finally:
        await file.close()
