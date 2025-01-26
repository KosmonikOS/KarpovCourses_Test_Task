import os
import numpy as np
from app.vector_store import VectorStore
from tests.constants import TEST_TEXT, TEST_EMBEDDING


def test_add_and_verify():
    """Test adding text and embedding to vector store and verifying it's there"""
    store = VectorStore(384)
    
    # Convert embedding to numpy array
    embeddings = np.array(TEST_EMBEDDING, dtype=np.float32)
    
    # Add test text and embedding
    store.add_texts([TEST_TEXT], embeddings)
    
    # Search with the same embedding - should return our text with high similarity
    query_embedding = np.array(TEST_EMBEDDING[0], dtype=np.float32)
    results = store.similarity_search(query_embedding, k=1)
    assert len(results) == 1
    assert results[0]["chunk"] == TEST_TEXT  # First result should be our text
    assert np.isclose(results[0]["score"], 1.0, rtol=1e-5)  # Similarity should be 1.0


def test_save_and_load():
    """Test saving and loading vector store preserves all data"""
    store = VectorStore(384)
    
    # Convert embedding to numpy array
    embeddings = np.array(TEST_EMBEDDING, dtype=np.float32)
    
    # Add test data
    store.add_texts([TEST_TEXT], embeddings)
    
    # Save to a temporary file
    temp_file = "temp_vector_store.faiss"
    store.save(temp_file)
    
    try:
        # Create new store and load data
        new_store = VectorStore(384)
        new_store.load(temp_file)
        
        # Verify data is preserved by searching
        query_embedding = np.array(TEST_EMBEDDING[0], dtype=np.float32)
        results = new_store.similarity_search(query_embedding, k=1)
        assert len(results) == 1
        assert results[0]["chunk"] == TEST_TEXT
        assert np.isclose(results[0]["score"], 1.0, rtol=1e-5)
    
    finally:
        # Clean up temp file
        if os.path.exists(temp_file):
            os.remove(temp_file)


def test_cosine_similarity():
    """Test that querying with the same text returns perfect similarity"""
    store = VectorStore(384)
    
    # Convert embedding to numpy array
    embeddings = np.array(TEST_EMBEDDING, dtype=np.float32)
    
    # Add test text and embedding
    store.add_texts([TEST_TEXT], embeddings)
    
    # Search with the same embedding
    query_embedding = np.array(TEST_EMBEDDING[0], dtype=np.float32)
    results = store.similarity_search(query_embedding, k=1)
    
    # Verify cosine similarity is 1.0 (perfect match)
    assert len(results) == 1
    similarity_score = results[0]["score"]
    assert np.isclose(
        similarity_score, 1.0, rtol=1e-5
    ), f"Expected similarity score 1.0, got {similarity_score}"
