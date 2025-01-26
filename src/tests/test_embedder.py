import numpy as np
from app.embedder import Embedder
from tests.constants import TEST_TEXT, TEST_EMBEDDING


def test_text_embedding():
    """Test that embedder produces consistent embeddings for a predefined text"""
    embedder = Embedder()
    embedding = embedder.get_embeddings(TEST_TEXT)

    # Convert both to numpy arrays for comparison and reshape to match
    actual = np.array(embedding)  # Shape: (384,)
    expected = np.array(TEST_EMBEDDING[0])  # Get first embedding and make it 1D

    # Check shape
    assert actual.shape == expected.shape, f"Expected shape {expected.shape}, got {actual.shape}"

    # Check values are close (using small tolerance due to floating point precision)
    np.testing.assert_allclose(
        actual,
        expected,
        rtol=1e-5,
        atol=1e-5,
        err_msg="Embedding values don't match expected values",
    )


def test_embedding_size():
    """Test that embedder produces embeddings of the correct size"""
    embedder = Embedder()
    embedding = embedder.get_embeddings(TEST_TEXT)
    assert len(embedding) == 384, f"Expected embedding size 384, got {len(embedding)}"
