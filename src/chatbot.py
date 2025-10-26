import os
import logging
from dotenv import load_dotenv

from lightrag.core.rag_chain import RAGChain
from lightrag.core.pipeline import Pipeline
from lightrag.core.components import Embedding, VectorStore, Generator
from lightrag.components.retriever import SimpleRetriever
from lightrag.components.data_process import SimpleTextProcessor
from lightrag.components.model import get_model
from lightrag.utils import setup_logger

# Load environment variables from .env file
load_dotenv()

# Setup logging
logger = setup_logger(__name__)

# --- Configuration from Environment Variables ---
KNOWLEDGE_BASE_PATH = os.path.join(os.getcwd(), 'src', 'data', 'knowledge_base.txt')
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "gpt-4.1-mini")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "text-embedding-ada-002")

class CustomerSupportChatbot:
    def __init__(self):
        # Simple in-memory storage for conversation history (for Context7-like dynamic context)
        self.history = [] 
        self.max_history_turns = 3 # Keep last 3 turns
        self.pipeline = self._setup_pipeline()
        logger.info("Chatbot initialized and knowledge base loaded.")

    def _load_knowledge_base(self):
        """Loads and processes the knowledge base text file."""
        try:
            with open(KNOWLEDGE_BASE_PATH, 'r', encoding='utf-8') as f:
                text = f.read()
            
            text_processor = SimpleTextProcessor(
                chunk_size=512,
                chunk_overlap=50,
                separator='\n\n',
            )
            documents = text_processor.process_texts([text])
            logger.info(f"Loaded and processed {len(documents)} documents from knowledge base at {KNOWLEDGE_BASE_PATH}")
            return documents
        except FileNotFoundError:
            logger.error(f"Knowledge base file not found at {KNOWLEDGE_BASE_PATH}")
            return []

    def _setup_pipeline(self):
        """Sets up the LightRAG RAGChain pipeline."""
        
        documents = self._load_knowledge_base()
        if not documents:
            raise RuntimeError("Failed to load knowledge base. Cannot initialize chatbot.")

        # Components
        generator = Generator(
            model=get_model(LLM_MODEL_NAME),
            system_prompt="You are an expert customer support agent for NovaPay. Answer the user's question based ONLY on the provided context. If the context does not contain the answer, politely state that you do not have the information."
        )

        embedding = Embedding(model=get_model(EMBEDDING_MODEL_NAME))

        vector_store = VectorStore(embedding=embedding)
        vector_store.add(documents)
        
        retriever = SimpleRetriever(vector_store=vector_store, top_k=3)
        
        rag_chain = RAGChain(
            retriever=retriever,
            generator=generator,
        )

        pipeline = Pipeline(rag_chain)
        return pipeline

    def _get_contextual_query(self, query: str) -> str:
        """
        Prepares a query with conversational history for better context.
        This simulates the dynamic context management (MCP pattern).
        """
        context = "\n".join(self.history)
        if context:
            full_query = f"Conversation History:\n{context}\n\nUser Query: {query}"
            return full_query
        return query

    def get_response(self, query: str) -> str:
        """Generates a response for a given user query and updates history."""
        if not query:
            return "Please provide a question."
        
        # 1. Prepare contextual query
        contextual_query = self._get_contextual_query(query)
        
        try:
            # 2. Run RAG pipeline
            response = self.pipeline.run(query=contextual_query)
            response_text = response.response
            
            # 3. Update history (MCP-like dynamic context)
            self.history.append(f"User: {query}")
            self.history.append(f"Agent: {response_text}")
            # Keep only the last N turns
            self.history = self.history[-self.max_history_turns * 2:] 
            
            return response_text
            
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
    # Simple test for the new conversational flow
    if CHATBOT:
        print("--- Chatbot Contextual Test ---")
        test_queries = [
            "I want to know about the fees.",
            "Specifically, what are the fees for domestic transfers?",
            "And what is the maximum limit for verified accounts?",
        ]
        
        for query in test_queries:
            print(f"\nQ: {query}")
            response = CHATBOT.get_response(query)
            print(f"A: {response}")
    else:
        print("Chatbot failed to initialize.")
