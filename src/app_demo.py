import streamlit as st
import os
import logging
from dotenv import load_dotenv

# Load environment variables (needed for Streamlit to access LLM keys)
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Import Chatbot (assuming it's in the same directory structure) ---
# Note: We import the class and re-initialize it to avoid issues with Streamlit's rerun nature.
# In a real production app, we would call the Flask API, but for a simple demo MVP, direct import is faster.
try:
    from .chatbot import CustomerSupportChatbot
except ImportError:
    # Handle case where Streamlit runs the file directly (no package context)
    st.error("Error: Could not import chatbot core. Please ensure Streamlit is run from the project root.")
    st.stop()


# --- Streamlit Session State Management ---

@st.cache_resource
def get_chatbot_instance():
    """Initializes the chatbot once and caches the instance."""
    try:
        return CustomerSupportChatbot()
    except Exception as e:
        st.error(f"Failed to initialize Chatbot. Check your API keys in the .env file or Hugging Face secrets. Error: {e}")
        logger.error(f"Chatbot initialization failed: {e}")
        return None

if 'messages' not in st.session_state:
    st.session_state.messages = []

# --- Streamlit UI ---

st.set_page_config(page_title="NovaPay Customer Support Chatbot Demo", layout="wide")

st.title("🤖 NovaPay Customer Support Agent (Demo MVP)")
st.caption("Powered by LangChain and Modular RAG Architecture")

# Get the cached chatbot instance
chatbot = get_chatbot_instance()

if chatbot:
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Спросите что-нибудь о NovaPay..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Думаю..."):
                response = chatbot.get_response(prompt)
            st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Sidebar for Configuration Info
    with st.sidebar:
        st.header("Конфигурация")
        st.success("Чат-бот успешно инициализирован!")
        st.markdown(f"**LLM Модель:** `{os.getenv('LLM_MODEL_NAME', 'Не задана')}`")
        st.markdown(f"**Векторная БД:** `ChromaDB (Local)`")
        st.markdown("**Архитектура:** LangChain RAG (Модульная)")
        st.markdown("---")
        st.info("Для смены LLM или подключения к Pinecone/Weaviate, измените переменные в `Secrets` на Hugging Face.")

else:
    st.warning("Чат-бот не запущен. Пожалуйста, проверьте переменные окружения (API ключи).")
