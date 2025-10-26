# NovaPay Customer Support Chatbot: Modern RAG API

## Overview

This repository provides a production-ready, context-aware RAG (Retrieval-Augmented Generation) chatbot designed for **NovaPay** customer support. It is built for **quick deployment (quick win)** and seamless integration with enterprise systems like **1C** and **Bitrix24**.

The core of this solution is a modern RAG pipeline powered by the **LightRAG** framework, exposed via a robust **Flask/Gunicorn** RESTful API.

### Key Modernizations & Features

| Feature | Description | Benefit |
| :--- | :--- | :--- |
| **Dynamic Context Management** | Implements a simple conversational memory to maintain context across multiple user queries. This mimics the **Model Context Protocol (MCP)** pattern, similar to "Context7," for more natural and relevant multi-turn conversations. | **Expert-Level Interaction:** Allows the chatbot to follow up on previous questions, significantly improving the user experience for complex inquiries. |
| **Easy Configuration (.env)** | All sensitive credentials and configuration settings are managed via a `.env` file. | **Fork-Ready:** Simplifies setup for new users and ensures security by keeping secrets out of the repository. |
| **RESTful API** | Exposes a simple `/api/v1/query` endpoint. | **Universal Integration:** The API can be consumed by any modern system, including webhooks from Bitrix24 and direct calls from 1C. |
| **Lightweight Deployment** | Containerized with `Dockerfile` and optimized for platforms like Hugging Face Spaces. | **Fast Time-to-Market:** Enables rapid deployment and iteration with minimal infrastructure overhead. |

## Quick Start for Forking

The project is designed to be **fork-ready**. You can deploy your own version of this customer support agent in minutes.

### 1. Setup Configuration

1.  **Fork** this repository to your own GitHub account.
2.  **Clone** your forked repository locally.
3.  **Create `.env` file:** Copy the example file and fill in your credentials.
    ```bash
    cp .env.example .env
    ```
4.  **Edit `.env`:** Open the new `.env` file and replace the placeholder values with your actual API key and desired model names.

    ```ini
    # .env
    OPENAI_API_KEY="YOUR_LLM_API_KEY_HERE"
    LLM_MODEL_NAME="gpt-4.1-mini"
    EMBEDDING_MODEL_NAME="text-embedding-ada-002"
    # ... other settings
    ```

### 2. Local Development

1.  **Setup Virtual Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
2.  **Run the Flask App:**
    ```bash
    python src/app.py
    ```
    The API will start on `http://127.0.0.1:5000`.

## Integration Strategy

The API-first architecture allows for flexible integration into various enterprise workflows.

### 1. Bitrix24 Integration (Customer-Facing)

This setup automates customer service directly in Bitrix24 Open Lines (e.g., WhatsApp, Telegram, VK).

| Component | Role | Integration Method |
| :--- | :--- | :--- |
| **Bitrix24 Open Lines** | Customer communication channel. | **Bitrix24 Chatbot API & Webhooks.** Bitrix is configured to send the user's message to our API. |
| **NovaPay Chatbot API** | Processes the query, uses RAG and conversational memory, and returns the answer. | Bitrix sends a POST request to `[YOUR_API_URL]/api/v1/query`. |

### 2. 1C Integration (Back-Office/Internal Support)

This provides instant, accurate internal support for sales or support agents using the 1C system.

| Component | Role | Integration Method |
| :--- | :--- | :--- |
| **1C System** | Internal user interface. | **Direct REST API Call.** 1C's business logic is programmed to make a call to our API. |
| **NovaPay Chatbot API** | Provides instant answers to internal queries about policies, transaction limits, or procedures. | 1C makes a POST request to `[YOUR_API_URL]/api/v1/query` and processes the JSON response. |

### Example API Usage (cURL)

You can test the API functionality using a simple cURL command:

```bash
curl -X POST http://127.0.0.1:5000/api/v1/query \
-H "Content-Type: application/json" \
-d '{"query": "What are the transaction fees for domestic transfers?"}'
```

## Project Structure

```
.
├── .env.example              # Template for environment variables (API keys, model names)
├── .gitignore                # Files to ignore (venv, .env, cache)
├── Dockerfile                # Docker configuration for Hugging Face deployment
├── README.md                 # Project documentation and use cases
├── requirements.txt          # Python dependencies
└── src/
    ├── __init__.py           # Python package marker
    ├── app.py                # Flask API application (runs the service)
    ├── chatbot.py            # Core LightRAG RAG and Context Management logic
    └── data/
        └── knowledge_base.txt  # The source of truth for RAG (editable knowledge base)
```

## Knowledge Base

The RAG system uses the information contained in `src/data/knowledge_base.txt`. To update the chatbot's knowledge, simply edit this file and redeploy the application. This allows for rapid content updates without touching the core code.

---
*This project is a rapid prototype developed by the NovaPay team to showcase modern AI integration capabilities.*
