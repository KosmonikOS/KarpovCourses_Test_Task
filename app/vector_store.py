import numpy as np
import faiss
import json
from numpy.typing import NDArray


class VectorStore:
    def __init__(self, dimension: int):
        """Initialize FAISS index
        Args:
            dimension: Dimension of the vectors (depends on the embedder model)
        """
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.texts: list[str] = []

    def add_texts(self, texts: list[str], embeddings: NDArray[np.float32]) -> None:
        """Add texts and their embeddings to the index
        Args:
            texts: List of texts to add
            embeddings: Array of embeddings as float32
        """
        if not texts or embeddings.size == 0:
            return

        self.index.add(embeddings)
        self.texts.extend(texts)

    def similarity_search(
        self, query_embedding: NDArray[np.float32], k: int = 5
    ) -> list[dict[str, float]]:
        """Search for most similar vectors using L2 distance
        Args:
            query_embedding: Query embedding as float32 array
            k: Number of results to return (will be capped by number of stored texts)
        Returns:
            List of dictionaries containing chunk and score for all retrieved chunks
        """
        # Ensure query embedding is 2D
        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)
            
        # Limit k to the number of stored texts
        k = min(k, len(self.texts))
        
        if k == 0:
            return []

        # Get nearest neighbors
        distances, indices = self.index.search(query_embedding, k)

        # Convert to list of dictionaries with text content and similarity score
        return [
            {"chunk": self.texts[idx], "score": float(score)}
            for idx, score in zip(indices[0], distances[0])
        ]

    def save(self, path: str) -> None:
        """Save the vector store to files
        Args:
            path: Base path for saving files (without extension)
        """
        # Save FAISS index
        index_path = f"{path}.faiss"
        faiss.write_index(self.index, index_path)
        
        # Save texts
        texts_path = f"{path}.json"
        with open(texts_path, 'w', encoding='utf-8') as f:
            json.dump(self.texts, f, ensure_ascii=False, indent=2)

    def load(self, path: str) -> None:
        """Load the vector store from files
        Args:
            path: Base path for loading files (without extension)
        """
        # Load FAISS index
        index_path = f"{path}.faiss"
        self.index = faiss.read_index(index_path)
        
        # Load texts
        texts_path = f"{path}.json"
        with open(texts_path, 'r', encoding='utf-8') as f:
            self.texts = json.load(f)
