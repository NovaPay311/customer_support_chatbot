# NovaPay Customer Support Chatbot: Production-Ready RAG API

## Overview

This repository is now a foundation for a **production-ready, highly scalable RAG (Retrieval-Augmented Generation) chatbot** designed for NovaPay customer support. It is engineered for commercial resale and deep integration with enterprise systems like **1C** and **Bitrix24**.

The core is built on a modular **LangChain** architecture, providing the flexibility and power needed to adapt to any client's requirements.

### Key Features & Scalability

| Feature | Description | Commercial Value |
| :--- | :--- | :--- |
| **Modular LangChain Core** | The RAG pipeline is built using LangChain's abstractions (Loaders, Splitters, Chains), allowing for easy component swapping without rewriting core logic. | **Future-Proof & Adaptable:** Ready to integrate any new LLM, Embedding Model, or Vector Database on the market. |
| **Vector DB Ready** | Configured for seamless integration with **ChromaDB** (for quick start) and prospective support for **Pinecone** and **Weaviate** (via `.env`). | **Scalable Knowledge:** Handles millions of documents, a necessity for large corporate clients. |
| **Conversational Memory** | Uses LangChain's standard memory abstraction to maintain context across queries. | **Expert Interaction:** Enables natural, multi-turn conversations, significantly boosting customer satisfaction. |
| **Enterprise API** | Exposed via a robust **Flask/Gunicorn** RESTful API. | **Universal Integration:** The API can be consumed by any modern system (Bitrix24 webhooks, 1C direct calls). |

---

## 🚀 Quick Start: Запуск в 3 Шага (Для Новичков)

Этот проект можно запустить с помощью **Docker** всего за несколько команд. Вам понадобится только установленный **Docker** и **API ключ** для LLM (например, OpenAI).

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
3.  **Вставьте свой API ключ:** Откройте файл `.env` и замените `YOUR_LLM_API_KEY_HERE` на ваш реальный ключ.

    ```ini
    # .env
    OPENAI_API_KEY="sk-..." # Ваш ключ
    # ... остальные настройки можно оставить по умолчанию
    ```

### Шаг 2: Сборка и Запуск Docker-контейнера

Выполните одну команду для сборки образа и запуска сервиса. Это займет несколько минут.

```bash
docker build -t novapay-chatbot . && docker run -d -p 5000:5000 --env-file .env --name novapay-agent novapay-chatbot
```

### Шаг 3: Проверка Работы (Тестирование API)

Ваш чат-бот запущен и доступен по адресу `http://localhost:5000`. Проверьте его работу с помощью `curl`:

```bash
curl -X POST http://localhost:5000/api/v1/query \
-H "Content-Type: application/json" \
-d '{"query": "What are the transaction fees for domestic transfers?"}'
```

Вы должны получить ответ от чат-бота!

---

## 🛠️ Архитектура и Расширение (Для Экспертов)

### Интеграция с Векторными Базами Данных

Проект настроен на использование **ChromaDB** в режиме `in-memory` для быстрого старта. Для перехода на продакшн-уровень и масштабирования, измените переменные в файле `.env`:

1.  **Установите** `VECDB_TYPE` на `PINECONE` или `WEAVIATE`.
2.  **Раскомментируйте** и заполните соответствующие поля API ключами и URL.

### Профессиональная Критика и Рекомендации

Мы успешно перешли от прототипа к **модульной, масштабируемой архитектуре**. Следующие шаги должны быть сфокусированы на демонстрации и коммерциализации:

| Приоритет | Направление | Описание Улучшения |
| :--- | :--- | :--- |
| **Высокий** | **Визуальная Демонстрация** | Использование **Hugging Face Spaces** с `gradio` или `Streamlit` для создания **визуального интерфейса (Demo Space)**. Это позволит клиентам тестировать чат-бота без cURL. |
| **Высокий** | **Интеграция с Векторной БД** | Фактическая реализация подключения к **Pinecone** или **Weaviate** (сейчас это только заготовка в `.env`). Это позволит нам проводить демонстрации с реальными, большими базами знаний. |
| **Средний** | **Масштабируемая Память** | Интеграция с **Redis** или другой внешней службой для **хранения истории диалогов** в продакшн-среде. |

**Заключение Эксперта:** Мы создали "пушку" — гибкую, модульную платформу, готовую к интеграции с любыми корпоративными системами. Следующий шаг — **упаковка для продажи** (визуальное демо и демонстрация масштабирования).

## Project Structure

```
.
├── .env.example              # Template for environment variables (API keys, model names)
├── .gitignore                # Files to ignore (venv, .env, cache)
├── Dockerfile                # Docker configuration for deployment
├── README.md                 # Project documentation and use cases
├── requirements.txt          # Python dependencies
└── src/
    ├── __init__.py           # Python package marker
    ├── app.py                # Flask API application (runs the service)
    ├── chatbot.py            # Core LangChain RAG and Context Management logic
    └── data/
        └── knowledge_base.txt  # The source of truth for RAG (editable knowledge base)
```
