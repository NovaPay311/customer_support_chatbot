# NovaPay Customer Support Chatbot: Production-Ready RAG Platform

## Overview

This repository is now a foundation for a **production-ready, highly scalable RAG (Retrieval-Augmented Generation) chatbot** designed for NovaPay customer support. It is engineered for commercial resale and deep integration with enterprise systems like **1C** and **Bitrix24**.

The core is built on a modular **LangChain** architecture, providing the flexibility and power needed to adapt to any client's requirements.

### Key Features & Scalability

| Feature | Description | Commercial Value |
| :--- | :--- | :--- |
| **Multi-LLM Support** | Dynamically switches between **OpenAI, Google (Gemini), and Anthropic (Claude)** models based on configuration. | **Flexibility & Cost Optimization:** Allows clients to choose the best model for their budget and performance needs. |
| **Modular LangChain Core** | The RAG pipeline is built using LangChain's abstractions, allowing for easy component swapping. | **Future-Proof & Adaptable:** Ready to integrate any new LLM, Embedding Model, or Vector Database on the market. |
| **Vector DB Ready** | Configured for seamless integration with **ChromaDB** (for quick start) and prospective support for **Pinecone** and **Weaviate** (via `.env`). | **Scalable Knowledge:** Handles millions of documents, a necessity for large corporate clients. |
| **Conversational Memory** | Uses LangChain's standard memory abstraction to maintain context across queries. | **Expert Interaction:** Enables natural, multi-turn conversations, significantly boosting customer satisfaction. |

---

## 🚀 Quick Start: Запуск Визуального Демо (Demo MVP)

Мы создали **визуальный интерфейс на Streamlit**, чтобы вы могли запустить и проверить работу чат-бота всего за несколько команд.

### Шаг 1: Клонирование и Настройка

1.  **Клонируйте** репозиторий:
    ```bash
    git clone https://github.com/NovaPay311/customer_support_chatbot.git
    cd customer_support_chatbot
    ```
2.  **Создайте файл `.env`** из шаблона:
    ```bash
    cp .env.example .env
    ```
3.  **Вставьте свой API ключ:** Откройте файл `.env` и вставьте **хотя бы один** LLM API ключ (например, `OPENAI_API_KEY`).

    ```ini
    # .env
    OPENAI_API_KEY="sk-..." # Ваш ключ
    # LLM_MODEL_NAME="gemini-2.5-flash" # Раскомментируйте, если используете Gemini
    ```

### Шаг 2: Сборка и Запуск Docker-контейнера

Выполните одну команду для сборки образа и запуска сервиса. **Демо-версия запустится на порту 8501.**

```bash
docker build -t novapay-chatbot . && docker run -d -p 8501:8501 --env-file .env --name novapay-agent novapay-chatbot
```

### Шаг 3: Проверка Работы (Визуальное Демо)

Откройте в браузере адрес: `http://localhost:8501`

Вы увидите полнофункциональный чат-интерфейс, готовый к демонстрации клиентам!

---

## 🛠️ Архитектура и Расширение (Для Экспертов)

### Многомодельная Поддержка (Multi-LLM)

Для смены модели просто измените переменные окружения:

1.  Убедитесь, что соответствующий API ключ (например, `GEMINI_API_KEY`) задан в `.env` или в секретах развертывания.
2.  Измените `LLM_MODEL_NAME` на желаемую модель (например, `gpt-4o`, `gemini-2.5-flash`, `claude-3-opus`).

### Интеграция с Векторными Базами Данных

Проект настроен на использование **ChromaDB** в режиме `in-memory` для быстрого старта. Для перехода на продакшн-уровень и масштабирования, измените переменные в файле `.env`:

1.  **Установите** `VECDB_TYPE` на `PINECONE` или `WEAVIATE`.
2.  **Раскомментируйте** и заполните соответствующие поля API ключами и URL.

### Профессиональная Критика и Рекомендации

Мы создали "пушку" — гибкую, модульную платформу, готовую к интеграции с любыми корпоративными системами. Следующий шаг — **упаковка для продажи** (финальное развертывание на Hugging Face).

## Project Structure

```
.
├── .env.example              # Template for environment variables (API keys, model names, DBs)
├── .dockerignore             # Files to ignore when building Docker image (venv, cache)
├── .gitignore                # Files to ignore (venv, .env, cache)
├── context7.json             # Context7 configuration for documentation indexing
├── Dockerfile                # Docker configuration for Streamlit Demo MVP
├── README.md                 # Project documentation and use cases
├── requirements.txt          # Python dependencies
└── src/
    ├── __init__.py           # Python package marker
    ├── app.py                # Original Flask API (still available for direct integration)
    ├── app_demo.py           # Streamlit Visual Demo MVP
    ├── chatbot.py            # Core LangChain RAG and Multi-LLM logic
    └── data/
        └── knowledge_base.txt  # The source of truth for RAG (editable knowledge base)
```
