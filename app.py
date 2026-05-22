import streamlit as st
import requests

st.title("RAG Application")

st.sidebar.header("Document Manager")

uploaded_file = st.sidebar.file_uploader("Upload a PDF", type="pdf")

if st.sidebar.button("Upload"):
    if uploaded_file is not None:
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}

        response = requests.post("http://127.0.0.1:8000/upload/", files=files)

        if response.status_code == 200:
            st.sidebar.success(f"Successfully uploaded: {uploaded_file.name}")
            st.session_state["current_file"] = uploaded_file.name


if "current_file" in st.session_state:
    st.subheader(f"Currently querying: {st.session_state['current_file']}")
    user_question = st.text_input("Question: ")
    if st.button("Search"):
        response = requests.post(
            "http://127.0.0.1:8000/search/",
        json={"question":user_question,
              "filename": st.session_state["current_file"]})
        data = response.json()

        st.write(data["ai_answer"])

        st.write("Sources")
        for source in data["sources"]:
            with st.expander(f"Page {source['metadata']['page_no']}"):
                st.write(source["text"])