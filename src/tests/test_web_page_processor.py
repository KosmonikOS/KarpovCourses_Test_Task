import pytest
from app.web_page_processor import WebPageProcessor
from app.config import COURSE_URLS
from tests.constants import EXPECTED_CHUNK_COUNT, EXPECTED_FIRST_CHUNKS


def test_chunk_count():
    """Test that processing first URL produces expected number of chunks"""
    processor = WebPageProcessor(chunk_size=500, chunk_overlap=100)
    chunks = processor.process_urls([COURSE_URLS[0]])
    assert len(chunks) == EXPECTED_CHUNK_COUNT


def test_first_chunks_content():
    """Test that first 5 chunks match expected content exactly"""
    processor = WebPageProcessor(chunk_size=500, chunk_overlap=100)
    chunks = processor.process_urls([COURSE_URLS[0]])

    # Compare first 5 chunks with expected content
    for actual, expected in zip(chunks[:5], EXPECTED_FIRST_CHUNKS):
        assert (
            actual.strip() == expected.strip()
        ), f"Chunk content mismatch:\nExpected: {expected}\nActual: {actual}"
