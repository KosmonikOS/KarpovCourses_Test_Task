from web_page_processor import WebPageProcessor
from course_advisor import CourseAdvisor
from vector_store import VectorStore
from config import COURSE_URLS
from dotenv import load_dotenv
from embedder import Embedder
import streamlit as st
import os

load_dotenv()

# Constants
vector_store_path = os.getenv("VECTOR_STORE_PATH")

# Set page config
st.set_page_config(page_title="Навигатор по курсам", page_icon="🎓", layout="wide")

# Title
st.title("Навигатор по курсам Karpov.Courses")
st.write("Задайте вопрос о курсах и получите персонализированную рекомендацию!")

# Initialize session state for vectorstore and advisor
if "advisor" not in st.session_state:

    @st.cache_resource(show_spinner=False)
    def initialize_advisor():
        # Initialize embedder
        embedder = Embedder()

        # Initialize or load vectorstore
        if os.path.exists(f"{vector_store_path}.faiss"):
            vectorstore = VectorStore(dimension=embedder.get_embedding_dimension())
            vectorstore.load(vector_store_path)
        else:
            # Process documents
            processor = WebPageProcessor()
            chunks = processor.process_urls(COURSE_URLS)

            # Create embeddings and initialize vectorstore
            embeddings = embedder.get_embeddings(chunks)
            vectorstore = VectorStore(dimension=embedder.get_embedding_dimension())
            vectorstore.add_texts(chunks, embeddings)
            vectorstore.save(vector_store_path)

        # Initialize advisor
        return CourseAdvisor(vectorstore=vectorstore, embedder=embedder)

    with st.spinner("Инициализация базы знаний... Это может занять некоторое время."):
        st.session_state.advisor = initialize_advisor()

# Query input
query = st.text_input(
    "Введите ваш вопрос о курсах:",
    placeholder="например: В чем разница между аналитикой и дата-инжинирингом?",
)

# Search button
if st.button("Получить ответ") and query:
    with st.spinner("Анализирую ваш вопрос..."):
        response = st.session_state.advisor.process_query(query)
        st.write(response)
