import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from langchain_openai import ChatOpenAI, OpenAIEmbeddings

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")


def create_qa_chain(pdf_path):

    # 1. Load PDF
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    # 2. Split text
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    docs = splitter.split_documents(documents)

    # 3. Embeddings (OpenRouter-compatible OpenAI API style)
    embeddings = OpenAIEmbeddings(
        api_key=API_KEY,
        base_url="https://openrouter.ai/api/v1"
    )

    # 4. ALWAYS rebuild vectorstore (clean RAG design)
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local("vectorstore")

    # 5. Retriever
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # 6. LLM (OpenRouter)
    llm = ChatOpenAI(
        api_key=API_KEY,
        base_url="https://openrouter.ai/api/v1",
        model="openai/gpt-4o-mini",
        temperature=0
    )

    # 7. QA function
    def qa_chain(query):

        retrieved_docs = retriever.invoke(query)

        context = "\n\n".join([doc.page_content for doc in retrieved_docs])

        prompt = f"""
You are a helpful AI assistant.

Answer ONLY using the context below.

Context:
{context}

Question:
{query}
"""

        response = llm.invoke(prompt)
        return response.content

    return qa_chain