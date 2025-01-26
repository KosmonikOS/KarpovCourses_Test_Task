import numpy as np
from numpy.typing import NDArray
from sentence_transformers import SentenceTransformer
import torch


class Embedder:
    def __init__(
        self, model_name: str = "intfloat/multilingual-e5-small", device: str = None
    ):
        """Initialize the embedder with a SentenceTransformer model
        Args:
            model_name: Name of the model to use (default: intfloat/multilingual-e5-small)
            device: Device to use for inference (default: auto-detect)
        """
        self.device = (
            device
            if device
            else (
                "mps"
                if torch.backends.mps.is_available()
                else ("cuda" if torch.cuda.is_available() else "cpu")
            )
        )
        self.model = SentenceTransformer(model_name, device=self.device)

    def get_embeddings(self, texts: list[str]) -> NDArray[np.float32]:
        """Get embeddings for a list of texts
        Args:
            texts: List of texts to embed
        Returns:
            NDArray of embeddings as float32
        """
        try:
            # SentenceTransformer returns numpy array, just ensure float32 type
            embeddings = self.model.encode(texts)
            return embeddings.astype(np.float32)
        except Exception as e:
            print(f"Error getting embeddings: {e}")
            return np.array([], dtype=np.float32)

    def get_embedding_dimension(self) -> int:
        """Get the dimension of the embeddings"""
        return self.model.get_sentence_embedding_dimension()
