
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)


def generate_answer(question: str, retrieved_chunks: list) -> dict:

    if not retrieved_chunks:
        return {
            "answer": "I could not find relevant information in the uploaded documents.",
            "sources": []
        }

    context_parts = []
    sources = []

    for chunk in retrieved_chunks:
        context_parts.append(chunk["text"])

        source = {
            "file": chunk["source"],
            "page": chunk["page"]
        }

        if source not in sources:
            sources.append(source)

    context = "\n\n".join(context_parts)

    prompt = f"""
You are OrgBot, an AI assistant for answering questions
about an organisation.

Answer the user's question using ONLY the information
provided in the context.

Rules:
1. Do not invent or assume information.
2. If the answer is not available in the context,
   clearly say that the information is not available.
3. Keep the answer simple, clear and concise.
4. Understand questions written in English or Hinglish.
5. Do not include information from outside the context.

Context:
{context}

User Question:
{question}

Answer:
"""

    try:
        response = client.interactions.create(
            model="gemini-3.5-flash-lite",
            input=prompt
        )

        return {
            "answer": response.output_text,
            "sources": sources
        }

    except Exception as error:
        print("GEMINI ERROR:", repr(error))

        return {
            "answer": "Sorry, I could not generate an answer right now.",
            "sources": sources,
            "error": str(error)
        }
