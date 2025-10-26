import os
from lightrag.core.rag_chain import RAGChain
from lightrag.core.pipeline import Pipeline
from lightrag.core.components import Embedding, VectorStore, Generator
from lightrag.components.retriever import SimpleRetriever
from lightrag.components.data_process import SimpleTextProcessor
from lightrag.components.model import get_model
from lightrag.utils import setup_logger

# Setup logging
logger = setup_logger(__name__)

# --- Configuration ---
# Adjusted path to be relative to the project root for deployment environment
KNOWLEDGE_BASE_PATH = 'src/data/knowledge_base.txt'
# Using a small, fast model for quick deployment on Hugging Face Spaces (e.g., gpt-4.1-mini)
# Note: The actual model used will depend on the environment setup on Hugging Face.
MODEL_NAME = "gpt-4.1-mini" 

class CustomerSupportChatbot:
    def __init__(self):
        self.pipeline = self._setup_pipeline()
        logger.info("Chatbot initialized and knowledge base loaded.")

    def _load_knowledge_base(self):
        """Loads and processes the knowledge base text file."""
        # Need to ensure the path is correct from the root directory
        full_path = os.path.join(os.getcwd(), KNOWLEDGE_BASE_PATH)
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # Simple Text Processor for chunking the knowledge base
            text_processor = SimpleTextProcessor(
                chunk_size=512,
                chunk_overlap=50,
                separator='\n\n',
            )
            documents = text_processor.process_texts([text])
            logger.info(f"Loaded and processed {len(documents)} documents from knowledge base.")
            return documents
        except FileNotFoundError:
            logger.error(f"Knowledge base file not found at {full_path}")
            return []

    def _setup_pipeline(self):
        """Sets up the LightRAG RAGChain pipeline."""
        
        # 1. Load and process documents
        documents = self._load_knowledge_base()
        if not documents:
            raise RuntimeError("Failed to load knowledge base. Cannot initialize chatbot.")

        # 2. Components
        # Using a placeholder for embedding and generator, assuming the environment has the necessary setup
        
        # Generator (LLM)
        generator = Generator(
            model=get_model(MODEL_NAME),
            system_prompt="You are an expert customer support agent for NovaPay. Answer the user's question based ONLY on the provided context. If the context does not contain the answer, politely state that you do not have the information."
        )

        # Embedding (Placeholder - LightRAG will use a default if not specified, or we can use a local one)
        # For simplicity and quick deployment, we'll let LightRAG handle the default embedding.
        embedding = Embedding(model=get_model("text-embedding-ada-002"))

        # Vector Store (In-memory for simplicity)
        vector_store = VectorStore(embedding=embedding)
        vector_store.add(documents)
        
        # Retriever
        retriever = SimpleRetriever(vector_store=vector_store, top_k=3)
        
        # 3. RAG Chain
        rag_chain = RAGChain(
            retriever=retriever,
            generator=generator,
        )

        # 4. Pipeline
        pipeline = Pipeline(rag_chain)
        return pipeline

    def get_response(self, query: str) -> str:
        """Generates a response for a given user query."""
        if not query:
            return "Please provide a question."
        
        try:
            response = self.pipeline.run(query=query)
            # The response object from LightRAG has a 'response' attribute for the text answer
            return response.response
        except Exception as e:
            logger.error(f"Error during RAG pipeline execution: {e}")
            return "Sorry, an unexpected error occurred while processing your request. Please try again later."

# Global instance of the chatbot
try:
    CHATBOT = CustomerSupportChatbot()
except RuntimeError as e:
    logger.error(f"Fatal error during chatbot initialization: {e}")
    CHATBOT = None

if __name__ == "__main__":
    if CHATBOT:
        print("--- Chatbot Test ---")
        test_queries = [
            "What are the transaction fees for domestic transfers?",
            "How do I reset my password?",
            "What is the daily transfer limit for verified accounts?",
            "Tell me about the integration with Bitrix24.",
            "What is the capital of France?", # Out-of-context question
        ]
        
        for query in test_queries:
            print(f"\nQ: {query}")
            response = CHATBOT.get_response(query)
            print(f"A: {response}")
    else:
        print("Chatbot failed to initialize.")
