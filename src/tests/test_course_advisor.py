from app.course_advisor import CourseAdvisor
from app.web_page_processor import WebPageProcessor
from app.vector_store import VectorStore
from app.embedder import Embedder
from app.config import COURSE_URLS
from tests.constants import TEST_QUESTION, TEST_ANSWER
from dotenv import load_dotenv

load_dotenv()


def test_course_advisor_response():
    """Test complete course advisor workflow with a predefined question"""
    # Initialize components
    processor = WebPageProcessor()
    store = VectorStore(384)
    embedder = Embedder()
    advisor = CourseAdvisor(store, embedder)

    # Process first course URL and get chunks
    chunks = processor.process_urls([COURSE_URLS[0]])

    # Get embeddings for chunks
    embeddings = embedder.get_embeddings(chunks)

    # Add to vector store
    store.add_texts(chunks, embeddings)

    # Process query with temperature 0 for deterministic output
    response = advisor.process_query(
        TEST_QUESTION, temperature=0.0, max_completion_tokens=10
    )

    # Assert response matches expected answer
    assert (
        response.strip() == TEST_ANSWER.strip()
    ), f"Expected answer:\n{TEST_ANSWER}\n\nGot:\n{response}"
