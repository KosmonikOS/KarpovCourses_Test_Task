from typing import List
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


class WebPageProcessor:
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 100,
    ):
        """Initialize document processor
        Args:
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def process_urls(self, urls: List[str]) -> List[str]:
        """Load URLs and split into chunks
        Args:
            urls: List of URLs to process
        Returns:
            List of text chunks
        """
        # Load documents
        loader = WebBaseLoader(urls)
        docs = loader.load()

        # Split documents
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )
        chunks = splitter.split_documents(docs)

        # Extract text content from chunks
        return [chunk.page_content for chunk in chunks]
