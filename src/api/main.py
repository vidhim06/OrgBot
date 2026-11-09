
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

from src.document_processing.pdf_reader import extract_pages_from_pdf
from src.document_processing.text_chunker import chunk_pages
from src.document_processing.embedding_model import generate_embeddings
from src.document_processing.vector_store import VectorStore
from src.generation.qa_pipeline import answer_question
import time
app = FastAPI(title="OrgBot API")

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
def ask_question(request: QuestionRequest):
    return answer_question(request.question)



@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    total_start = time.perf_counter()
    stored_path = None

    try:
        if not file.filename or Path(file.filename).suffix.lower() != ".pdf":
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed."
            )

        # 1. Read PDF
        start = time.perf_counter()
        content = await file.read()
        print(f"1. File reading: {time.perf_counter() - start:.2f}s")

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

        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

        original_filename = Path(file.filename).name
        stored_path = UPLOAD_DIR / f"{uuid4().hex}.pdf"

        # 2. Save PDF
        start = time.perf_counter()
        stored_path.write_bytes(content)
        print(f"2. Saving PDF: {time.perf_counter() - start:.2f}s")

        # 3. Extract text
        start = time.perf_counter()
        pages = extract_pages_from_pdf(str(stored_path))
        print(f"3. PDF extraction: {time.perf_counter() - start:.2f}s")

        if not pages:
            raise HTTPException(
                status_code=400,
                detail="No readable text found in this PDF."
            )

        for page in pages:
            page["source"] = original_filename

        # 4. Create chunks
        start = time.perf_counter()
        chunks = chunk_pages(pages)
        print(f"4. Chunking: {time.perf_counter() - start:.2f}s")

        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="No text chunks could be created."
            )

        # 5. Generate embeddings
        start = time.perf_counter()
        embeddings = generate_embeddings(
            [chunk["text"] for chunk in chunks]
        )
        print(f"5. Embedding generation: {time.perf_counter() - start:.2f}s")

        # 6. Store in ChromaDB
        start = time.perf_counter()
        store = VectorStore()
        store.add_chunks(chunks, embeddings)
        print(f"6. ChromaDB storage: {time.perf_counter() - start:.2f}s")

        print(f"TOTAL UPLOAD TIME: {time.perf_counter() - total_start:.2f}s")

        return {
            "message": "PDF uploaded and processed successfully!",
            "filename": original_filename,
            "pages_processed": len(pages),
            "chunks_created": len(chunks)
        }

    except HTTPException:
        if stored_path:
            stored_path.unlink(missing_ok=True)
        raise

    except Exception as error:
        if stored_path:
            stored_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=500,
            detail=f"PDF processing failed: {str(error)}"
        )

    finally:
        await file.close()

    