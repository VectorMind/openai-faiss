import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

st.header("Content Question")
st.write("Enter text")

text_upload = st.file_uploader("Drop a text file",type="txt")
if text_upload is None:
    print("text is None")
    exit(0)

text = text_upload.getvalue().decode("utf-8")
st.write(text)

splitter = CharacterTextSplitter(
separator="\n",
chunk_size=1000,
chunk_overlap=200,
length_function=len
)
chunks = splitter.split_text(text)

st.header("Chunks")
st.write(chunks)

load_dotenv()

embeddings = OpenAIEmbeddings()
knowledge_base = FAISS.from_texts(chunks, embeddings)

question = st.text_input("Question")
if not question:
    exit(0)

references = knowledge_base.similarity_search(question)

st.header("Result")
st.write(references)

#llm = OpenAI()
#chain = load_qa_chain(llm, chain_type="stuff")
#with get_openai_callback() as cb:
#    response = chain.run(input_documents=references, question=user_question)
#    print(cb)
#    
#st.write(response)
