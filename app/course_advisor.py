import os
from openai import OpenAI
from config import QA_PROMPT
from vector_store import VectorStore
from embedder import Embedder


class CourseAdvisor:
    def __init__(self, vectorstore: VectorStore, embedder: Embedder):
        """Initialize course advisor with vector store and embedder
        Args:
            vectorstore: VectorStore instance for course content search
            embedder: Embedder instance for question embedding
        """
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL")
        )
        self.model = os.getenv("OPENAI_MODEL")
        self.vectorstore = vectorstore
        self.embedder = embedder

    def retrieve_context(self, question: str) -> list[str]:
        """Retrieve relevant course content for the question
        Args:
            question: Question about courses
        Returns:
            List of relevant course content chunks
        """
        # Get embedding for the question
        question_embedding = self.embedder.get_embeddings([question])

        # Search using similarity
        results = self.vectorstore.similarity_search(question_embedding)
        return [doc["chunk"] for doc in results]

    def generate_completion(self, question: str, context: str) -> str:
        """Generate course advice using OpenAI API
        Args:
            question: Question about courses
            context: Relevant course content to use for answering
        Returns:
            Generated course advice
        """
        try:
            # Format the prompt using the template
            formatted_prompt = QA_PROMPT.format(
                context=context,
                question=question
            )
            
            messages = [
                {"role": "user", "content": formatted_prompt}
            ]
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating course advice: {e}")
            return ""

    def process_query(self, question: str) -> str:
        """Process a course-related question and generate advice
        Args:
            question: Question about courses
        Returns:
            Generated course advice based on relevant content
        """
        # Get relevant context
        contexts = self.retrieve_context(question)
        context_str = "\n".join(contexts)
        
        # Generate and return answer
        return self.generate_completion(question, context_str) 