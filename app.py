import streamlit as st
from dotenv import load_dotenv
from pymongo import MongoClient
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub
import os


# Load environment variables
load_dotenv()

# Connect to MongoDB
client = MongoClient(os.getenv("MONGO_URI"))
db = client["your_database_name"]  # Replace "your_database_name" with your actual database name
users_collection = db["users"]

# Function to authenticate user
def authenticate(username, password):
    user = users_collection.find_one({"username": username, "password": password})
    return user is not None

# Function to sign up user
def signup(username, password):
    user = {"username": username, "password": password}
    users_collection.insert_one(user)

# Function to display login page
def login_page():
    st.write("""
        <style>
        .login-heading {
            text-align: center;
            background-color: #f0f0f0; /* You can change the background color here */
            padding: 20px;
            border-radius: 10px;
        }
        </style>
        <div class="login-heading">
            <h1>DataDive</h1>
        </div>
    """, unsafe_allow_html=True)
    st.write("<h2>Login</h2>", unsafe_allow_html=True)
    username_login = st.text_input("Username")
    password_login = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate(username_login, password_login):
            st.success("Login successful!")
            return True
        else:
            st.error("Invalid username or password")
    st.write("<h2>Signup</h2>", unsafe_allow_html=True)
    username_signup = st.text_input("Username (Signup)", key="signup_username")
    password_signup = st.text_input("Password (Signup)", type="password", key="signup_password")
    if st.button("Signup"):
        signup(username_signup, password_signup)
        st.success("Signup successful! You can now login.")
    return False

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)


def main():
    st.set_page_config(page_title="DataDive", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login_container = st.empty()
        if login_page():
            st.session_state.logged_in = True
            login_container.empty()  # Clear the login page if logged in
    else:
        st.header("DataDive :books:")
        user_question = st.text_input("Ask a question about your documents:")
        if user_question:
            handle_userinput(user_question)

        with st.sidebar:
            st.subheader("Your documents")
            pdf_docs = st.file_uploader(
                "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
            if st.button("Process"):
                with st.spinner("Processing"):
                    # get pdf text
                    raw_text = get_pdf_text(pdf_docs)

                    # get the text chunks
                    text_chunks = get_text_chunks(raw_text)

                    # create vector store
                    vectorstore = get_vectorstore(text_chunks)

                    # create conversation chain
                    st.session_state.conversation = get_conversation_chain(
                        vectorstore)

if __name__ == '__main__':
    main()
