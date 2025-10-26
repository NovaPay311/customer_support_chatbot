import os
import logging
from dotenv import load_dotenv

# --- LangChain Imports ---
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import TextLoader

# Load environment variables from .env file
load_dotenv()

# --- Configuration from Environment Variables ---
KNOWLEDGE_BASE_PATH = os.path.join(os.getcwd(), 'src', 'data', 'knowledge_base.txt')
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "gpt-4.1-mini")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "text-embedding-ada-002")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
VECDB_TYPE = os.getenv("VECDB_TYPE", "CHROMA")
CHROMA_PERSIST_DIRECTORY = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CustomerSupportChatbot:
    def __init__(self):
        if not OPENAI_API_KEY:
            logger.error("OPENAI_API_KEY is not set. Chatbot cannot be initialized.")
            raise ValueError("OPENAI_API_KEY is required.")
            
        self.chain = self._setup_chain()
        logger.info("Chatbot initialized with LangChain RAG architecture.")

    def _load_and_process_documents(self):
        """Loads and processes the knowledge base text file using LangChain components."""
        try:
            # Use TextLoader for simple file loading
            loader = TextLoader(KNOWLEDGE_BASE_PATH)
            documents = loader.load()
            
            # Use RecursiveCharacterTextSplitter for robust chunking
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                separators=["\n\n", "\n", " ", ""]
            )
            
            # Split documents into chunks
            texts = text_splitter.split_documents(documents)
            logger.info(f"Loaded and processed {len(texts)} chunks from knowledge base.")
            return texts
        except FileNotFoundError:
            logger.error(f"Knowledge base file not found at {KNOWLEDGE_BASE_PATH}")
            return []

    def _setup_vector_store(self, texts):
        """Sets up the vector store (ChromaDB for quick start)."""
        
        # Configure Embeddings
        embeddings = OpenAIEmbeddings(
            model=EMBEDDING_MODEL_NAME,
            openai_api_key=OPENAI_API_KEY,
            openai_api_base=OPENAI_API_BASE
        )
        
        # Use ChromaDB for quick start/local development
        if VECDB_TYPE == "CHROMA":
            vector_store = Chroma.from_documents(
                documents=texts,
                embedding=embeddings,
                persist_directory=CHROMA_PERSIST_DIRECTORY
            )
            # Persist the store to disk (optional, but good for quick restart)
            vector_store.persist()
            logger.info(f"ChromaDB vector store created and persisted to {CHROMA_PERSIST_DIRECTORY}")
            return vector_store
        
        # Placeholder for other vector DBs (e.g., Pinecone, Weaviate)
        else:
            logger.warning(f"Vector DB type {VECDB_TYPE} not fully implemented. Using in-memory Chroma.")
            return Chroma.from_documents(documents=texts, embedding=embeddings)

    def _setup_chain(self):
        """Sets up the LangChain ConversationalRetrievalChain."""
        
        texts = self._load_and_process_documents()
        if not texts:
            raise RuntimeError("Failed to load knowledge base. Cannot initialize chain.")

        vector_store = self._setup_vector_store(texts)
        
        # 1. LLM for Question Answering
        llm = ChatOpenAI(
            model=LLM_MODEL_NAME,
            temperature=0,
            openai_api_key=OPENAI_API_KEY,
            openai_api_base=OPENAI_API_BASE
        )
        
        # 2. Conversational Memory (In-memory for quick start, but ready for externalization)
        # This is the "Context7-like" feature, now using LangChain's standard memory abstraction.
        memory = ConversationBufferMemory(
            memory_key="chat_history", 
            return_messages=True,
            output_key="answer"
        )

        # 3. Custom Prompt (Ensuring the agent is professional and context-bound)
        custom_template = """You are an expert customer support agent for NovaPay. Your goal is to answer the user's question based ONLY on the provided context.
If the context does not contain the answer, politely state that you do not have the information.
The conversation history is provided below.

Chat History:
{chat_history}

Context:
{context}

Question: {question}
Answer:"""
        
        QA_CHAIN_PROMPT = PromptTemplate.from_template(custom_template)

        # 4. Conversational Retrieval Chain
        chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
            memory=memory,
            combine_docs_chain_kwargs={"prompt": QA_CHAIN_PROMPT},
            return_source_documents=False # Set to True for debugging/citation
        )
        
        return chain

    def get_response(self, query: str) -> str:
        """Generates a response for a given user query using the LangChain."""
        if not query:
            return "Please provide a question."
        
        try:
            # LangChain's chain.invoke handles the entire RAG cycle:
            # 1. Gets chat history from memory.
            # 2. Uses history and new question to retrieve relevant documents.
            # 3. Passes history, context, and question to the LLM.
            # 4. Stores new turn in memory.
            result = self.chain.invoke({"question": query})
            return result.get("answer", "Sorry, I couldn't process that request.")
            
        except Exception as e:
            logger.error(f"Error during LangChain RAG execution: {e}")
            # In a real app, you might want to reset the memory on error
            return "Sorry, an unexpected error occurred while processing your request. Please try again later."

# Global instance of the chatbot
try:
    CHATBOT = CustomerSupportChatbot()
except (RuntimeError, ValueError) as e:
    logger.error(f"Fatal error during chatbot initialization: {e}")
    CHATBOT = None

if __name__ == "__main__":
    # Simple test for the new conversational flow
    if CHATBOT:
        print("--- Chatbot Contextual Test (LangChain) ---")
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
