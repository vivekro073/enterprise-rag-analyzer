import uvicorn
import io
from fastapi import FastAPI, File, UploadFile
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from pydantic import BaseModel
from langchain_core.documents import Document
from google import genai
import os
from dotenv import load_dotenv

app = FastAPI()


@app.get("/")
def read_root():
    return {"status": "Enterprise RAG API is live"}


@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    file_content = await file.read()

    pdf_reader = PdfReader(io.BytesIO(file_content))

    all_text = []
    for page_num, pages in enumerate(pdf_reader.pages, start=1):
        text = pages.extract_text()
        page_content = Document(page_content=text, metadata={"page_no": page_num, "source": file.filename})
        all_text.append(page_content)

    #full_text = " ".join(all_text)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(all_text)

    model_name = "all-MiniLM-L6-v2"
    hf = HuggingFaceEmbeddings(
        model_name=model_name,
    )
    vectorstore = Chroma.from_documents(
        documents=texts,
        embedding=hf,
        persist_directory="./chroma_db"
    )

    return {
        "filename": file.filename,
        "message": "Extraction, chunking, and embedding successful.",
        "total_chunks": len(texts),
        "message2": "Success",
    }

class SearchRequest(BaseModel):
    question: str
    filename: str

@app.post("/search/")
def user_query(payload: SearchRequest):

    model_name = "all-MiniLM-L6-v2"
    hf = HuggingFaceEmbeddings(
        model_name=model_name
    )
    vectors = Chroma(persist_directory="./chroma_db",
                     embedding_function=hf,)

    results = vectors.max_marginal_relevance_search(
        query=payload.question,
        k=8,
        fetch_k=25,
        filter={"source":payload.filename},
    )

    all_results = []
    for result in results:
        all_results.append({"text": result.page_content,
                            "metadata": result.metadata,})

    context_text = "\n\n---\n\n".join([doc.page_content for doc in results])

    prompt = f"""
        You are a precise technical analyst. Answer the user's question using ONLY the context provided below. 
        If the exact answer is not contained in the context, you must respond with: "I cannot answer this based on the provided document."

        Context:
        {context_text}

        User Question: {payload.question}
        """

    load_dotenv()
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        ai_answer = response.text

    except Exception as e:
        print(f"⚠️ Gemini API Error caught: {e}")
        ai_answer = "Google Gemini is experiencing high demand, try again in some time."


    return {
        "question_asked": payload.question,
        "ai_answer": ai_answer,
        "sources": all_results,
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

















