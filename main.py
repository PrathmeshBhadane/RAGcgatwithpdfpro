import os
import shutil
from fastapi import FastAPI, UploadFile

from rag.pipeline import create_qa_chain

app = FastAPI()

qa_chain = None


# -------------------------
# UPLOAD PDF ENDPOINT
# -------------------------
@app.post("/upload/")
async def upload_pdf(file: UploadFile):

    global qa_chain

    # ✅ ensure folder exists
    os.makedirs("data", exist_ok=True)

    file_path = f"data/{file.filename}"

    # save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # create QA system
    qa_chain = create_qa_chain(file_path)

    return {
        "message": "PDF processed successfully",
        "filename": file.filename
    }


# -------------------------
# ASK QUESTION ENDPOINT
# -------------------------
@app.get("/ask/")
async def ask(query: str):

    global qa_chain

    if qa_chain is None:
        return {"answer": "Please upload a PDF first"}

    try:
        result = qa_chain(query)   # ✅ FIXED (no .run)
        return {"answer": result}

    except Exception as e:
        return {
            "answer": "Error processing query",
            "error": str(e)
        }