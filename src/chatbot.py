import os
import logging
from dotenv import load_dotenv

# --- LangChain Imports ---
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from .advanced_retrievers import get_hyde_retriever, get_rag_fusion_retriever
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
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
VECDB_TYPE = os.getenv("VECDB_TYPE", "CHROMA")
CHROMA_PERSIST_DIRECTORY = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def _get_llm_instance(model_name: str):
    """Dynamically selects and initializes the correct LLM based on model name and available API keys."""
    model_name = model_name.lower()

    if "gpt" in model_name or "openai" in model_name:
        if not OPENAI_API_KEY:
            raise ValueError("OpenAI model requested but OPENAI_API_KEY is not set.")
        logger.info(f"Using OpenAI model: {model_name}")
        return ChatOpenAI(
            model=model_name,
            temperature=0,
            openai_api_key=OPENAI_API_KEY,
            openai_api_base=OPENAI_API_BASE
        )
    elif "gemini" in model_name or "google" in model_name:
        if not GEMINI_API_KEY:
            raise ValueError("Gemini model requested but GEMINI_API_KEY is not set.")
        logger.info(f"Using Gemini model: {model_name}")
        return ChatGoogleGenerativeAI(
            model=model_name,
            temperature=0,
            google_api_key=GEMINI_API_KEY
        )
    elif "claude" in model_name or "anthropic" in model_name:
        if not ANTHROPIC_API_KEY:
            raise ValueError("Claude model requested but ANTHROPIC_API_KEY is not set.")
        logger.info(f"Using Anthropic model: {model_name}")
        return ChatAnthropic(
            model=model_name,
            temperature=0,
            anthropic_api_key=ANTHROPIC_API_KEY
        )
    else:
        raise ValueError(f"Unsupported model name or missing API key for: {model_name}. Check .env.example.")


class CustomerSupportChatbot:
    def __init__(self):
        self.use_hyde = os.getenv("USE_HYDE", "False").lower() == "true"
        self.use_rag_fusion = os.getenv("USE_RAG_FUSION", "False").lower() == "true"
        self.rag_fusion_k = int(os.getenv("RAG_FUSION_K", 4))
        self.rag_fusion_search = None # Инициализация для RAG-Fusion
        
        if not (OPENAI_API_KEY or GEMINI_API_KEY or ANTHROPIC_API_KEY):
            logger.error("No LLM API key is set. Chatbot cannot be initialized.")
            raise ValueError("At least one LLM API key (OpenAI, Gemini, or Anthropic) is required.")
            
        self.chain = self._setup_chain()
        
        if self.use_rag_fusion:
            # Инициализируем RAG-Fusion после настройки chain, чтобы использовать его компоненты
            from .advanced_retrievers import get_rag_fusion_retriever
            # Передаем базовый ретривер (который уже может быть HyDE-ретривером)
            self.rag_fusion_search = get_rag_fusion_retriever(
                llm=self._get_llm_instance(LLM_MODEL_NAME),
                base_retriever=self.chain.retriever,
                k_queries=self.rag_fusion_k
            )
            
        logger.info("Chatbot initialized with LangChain RAG architecture and Multi-LLM support.")
    def __init__(self):
        if not (OPENAI_API_KEY or GEMINI_API_KEY or ANTHROPIC_API_KEY):
            logger.error("No LLM API key is set. Chatbot cannot be initialized.")
            raise ValueError("At least one LLM API key (OpenAI, Gemini, or Anthropic) is required.")
            
        self.chain = self._setup_chain()
        logger.info("Chatbot initialized with LangChain RAG architecture and Multi-LLM support.")

    def _load_and_process_documents(self):
        """Loads and processes the knowledge base text file using LangChain components."""
        try:
            loader = TextLoader(KNOWLEDGE_BASE_PATH)
            documents = loader.load()
            
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                separators=["\n\n", "\n", " ", ""]
            )
            
            texts = text_splitter.split_documents(documents)
            logger.info(f"Loaded and processed {len(texts)} chunks from knowledge base.")
            return texts
        except FileNotFoundError:
            logger.error(f"Knowledge base file not found at {KNOWLEDGE_BASE_PATH}")
            return []

    def _setup_vector_store(self, texts):
        """Sets up the vector store (ChromaDB for quick start)."""
        
        # NOTE: We currently only support OpenAIEmbeddings as it's the most common.
        # For a full multi-LLM solution, we would need to dynamically load other embedding models.
        # For this MVP, we rely on OpenAI's embedding service.
        if not OPENAI_API_KEY:
             raise ValueError("OPENAI_API_KEY is required for embedding model initialization.")

        embeddings = OpenAIEmbeddings(
            model=EMBEDDING_MODEL_NAME,
            openai_api_key=OPENAI_API_KEY,
            openai_api_base=OPENAI_API_BASE
        )
        
        if VECDB_TYPE == "CHROMA":
            vector_store = Chroma.from_documents(
                documents=texts,
                embedding=embeddings,
                persist_directory=CHROMA_PERSIST_DIRECTORY
            )
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
        
        # 1. LLM for Question Answering (Dynamically selected)
        llm = _get_llm_instance(LLM_MODEL_NAME)
        
        # 2. Conversational Memory
        memory = ConversationBufferMemory(
            memory_key="chat_history", 
            return_messages=True,
            output_key="answer"
        )

        # 3. Custom Prompt
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
            retriever=vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 10} # Увеличиваем k для Reranking
        )

        # 5. Advanced RAG Techniques (HyDE and Reranking)
        if self.use_hyde:
            # HyDE должен быть применен к базовому ретриверу
            retriever = get_hyde_retriever(
                llm=llm,
                base_retriever=retriever,
                embedding_model=embeddings
            )
        
        # Reranking (если используется)
        cohere_api_key = os.getenv("COHERE_API_KEY")
        if cohere_api_key:
            from langchain.retrievers.document_compressors import CohereRerank
            from langchain.retrievers import ContextualCompressionRetriever

            compressor = CohereRerank(cohere_api_key=cohere_api_key, top_n=5)
            retriever = ContextualCompressionRetriever(
                base_compressor=compressor, base_retriever=retriever
            )

        # 6. Conversational Retrieval Chain
        chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever, # Используем модифицированный ретривер
            memory=memory,
            combine_docs_chain_kwargs={"prompt": QA_CHAIN_PROMPT},
            return_source_documents=False
        )
            memory=memory,
            combine_docs_chain_kwargs={"prompt": QA_CHAIN_PROMPT},
            return_source_documents=False
        )
        
        return chain

    def get_response(self, query: str) -> str:
        """Generates a response for a given user query using the LangChain."""
        if not query:
            return "Please provide a question."
        
        try:
            if self.use_rag_fusion:
            # Используем RAG-Fusion напрямую
            documents = self.rag_fusion_search(query)
            context = "\n".join([doc.page_content for doc in documents])
            
            # Генерируем ответ с использованием LLM и контекста
            # (упрощенная версия без ConversationalRetrievalChain)
            from langchain.prompts import PromptTemplate
            from langchain.chains import LLMChain

            prompt = PromptTemplate(
                input_variables=["context", "question"],
                template="""Используй следующий контекст для ответа на вопрос.
                Если ты не знаешь ответа, просто скажи, что не знаешь.

                Контекст: {context}

                Вопрос: {question}

                Ответ:"""
            )
            
            llm_chain = LLMChain(llm=self._get_llm_instance(LLM_MODEL_NAME), prompt=prompt)
            response = llm_chain.run(context=context, question=query)
            
            # Обновляем историю разговора вручную
            # self.chat_history.append((query, response)) # Не нужно, так как memory не используется
            return response
        else:
            # Стандартный RAG (с HyDE и Reranking, если включены)
            result = self.chain.invoke({"question": query})
            # Обновляем историю разговора через memory в chain, но возвращаем ответ
            return result.get("answer", "Sorry, I couldn't process that request.")
            return result.get("answer", "Sorry, I couldn't process that request.")
            
        except Exception as e:
            logger.error(f"Error during LangChain RAG execution: {e}")
            return "Sorry, an unexpected error occurred while processing your request. Please try again later."

# Global instance of the chatbot
try:
    CHATBOT = CustomerSupportChatbot()
except (RuntimeError, ValueError) as e:
    logger.error(f"Fatal error during chatbot initialization: {e}")
    CHATBOT = None
    
# Re-import CHATBOT in app.py to ensure the latest version is used
from .app import app # This line is just to make the linter happy, the actual app.py doesn't need to change yet.

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
