# NovaPay Customer Support Chatbot

## Overview

This repository contains the foundation for the NovaPay Customer Support Chatbot, built for rapid deployment and integration with enterprise systems like **1C** and **Bitrix24**.

The core of the chatbot is a **Retrieval-Augmented Generation (RAG)** system powered by the **LightRAG** framework. This choice prioritizes a "quick win" approach, allowing for fast iteration and deployment of a functional proof-of-concept.

### Key Features
- **RAG-based Answers:** Provides accurate, context-aware answers based on a dedicated knowledge base.
- **RESTful API:** Exposes a simple `/api/v1/query` endpoint for easy integration with external systems.
- **Lightweight Deployment:** Optimized for quick and cost-effective deployment on platforms like Hugging Face Spaces.

## Integration Strategy

The architecture is designed to be a central, intelligent API layer that can be consumed by various front-end and back-office systems.

### 1. Bitrix24 Integration (Customer-Facing)

The chatbot is designed to integrate seamlessly with **Bitrix24 Open Lines** using the native Bitrix24 Chatbot API and webhooks.

| Component | Role | Integration Method |
| :--- | :--- | :--- |
| **Bitrix24 Open Lines** | Customer communication channel (e.g., WhatsApp, Telegram). | Native Bitrix24 Chatbot API and Webhooks. |
| **NovaPay Chatbot API** | The RAG engine that processes the query and returns the answer. | Bitrix24 sends the user's message to the `/api/v1/query` endpoint via a webhook, and the response is sent back to the user. |

### 2. 1C Integration (Back-Office)

For back-office operations, such as providing internal support to sales or support agents, the 1C system can query the chatbot directly.

| Component | Role | Integration Method |
| :--- | :--- | :--- |
| **1C System** | Internal user interface or business logic. | Direct REST API call. |
| **NovaPay Chatbot API** | Provides instant answers to internal queries about policies, transaction limits, or procedures. | 1C makes a POST request to the `/api/v1/query` endpoint and processes the JSON response. |

## Deployment on Hugging Face Spaces

This project is configured to be deployed as a **Docker Space** on Hugging Face.

1.  **Create a New Space:** Choose "Docker" as the Space SDK.
2.  **Push Code:** Clone this repository locally and push the files (including `Dockerfile`, `src/`, and `requirements.txt`) to your Hugging Face Space repository.
3.  **Environment Variables:** The chatbot relies on an OpenAI-compatible API for the LLM and Embeddings. You must set the following environment variables in your Hugging Face Space settings:
    - `OPENAI_API_KEY`: Your API key for the chosen LLM provider.
    - `OPENAI_API_BASE`: The base URL for the API (e.g., `https://api.openai.com/v1` or a custom endpoint for a self-hosted model).

Once deployed, the API will be accessible at `[YOUR_SPACE_URL]/api/v1/query`.

## Getting Started (Local Development)

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/NovaPay311/customer_support_chatbot.git
    cd customer_support_chatbot
    ```
2.  **Setup Virtual Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
3.  **Run the Flask App:**
    ```bash
    python src/app.py
    ```
    The API will start on `http://127.0.0.1:5000`.

## Knowledge Base

The RAG system uses the information contained in `src/data/knowledge_base.txt`. To update the chatbot's knowledge, simply edit this file and redeploy the application.

---
*This project is a rapid prototype developed by the NovaPay team to showcase modern AI integration capabilities.*
