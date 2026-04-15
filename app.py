import streamlit as st
import requests

st.title("Chat with PDF (RAG + OpenRouter)")

API_URL = "http://localhost:8000"


# -----------------------
# UPLOAD SECTION
# -----------------------
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:
    try:
        with st.spinner("Uploading..."):
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file,
                    "application/pdf"
                )
            }

            res = requests.post(
                f"{API_URL}/upload/",
                files=files,
                timeout=60
            )

        if res.status_code == 200:
            st.success("PDF Uploaded & Processed!")
        else:
            st.error("Upload failed")
            st.write(res.text)

    except Exception as e:
        st.error(f"Connection error: {str(e)}")


# -----------------------
# CHAT SECTION
# -----------------------
query = st.text_input("Ask a question")

if query and query.strip():

    try:
        with st.spinner("Thinking..."):
            res = requests.get(
                f"{API_URL}/ask/",
                params={"query": query},
                timeout=60
            )

        if res.status_code == 200:
            try:
                data = res.json()
                st.write(data.get("answer", "No answer found"))
            except:
                st.error("Backend returned invalid JSON")
                st.write(res.text)
        else:
            st.error("Server error")
            st.write(res.text)

    except Exception as e:
        st.error(f"Backend not reachable: {str(e)}")