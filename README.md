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

## 🛠️ Для Разработчиков (Local Development)

Для тех, кто хочет работать с кодом напрямую:

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

## Профессиональная Критика и Рекомендации

Как эксперт, я вижу, что мы создали отличный, минимально жизнеспособный продукт (MVP) с акцентом на скорость и интеграцию. Вот мои **критические замечания и рекомендации** для дальнейшего развития:

### 1. Критика Текущего MVP

*   **Статичное Знание:** Вся база знаний находится в одном файле `knowledge_base.txt`. Это не масштабируется. Для реального бизнеса потребуется интеграция с базой данных или системой управления контентом.
*   **Простая Память:** Механизм "Context7-like" памяти (в `src/chatbot.py`) — это простой массив в памяти. Он сбрасывается при каждом перезапуске и не работает при горизонтальном масштабировании (когда запросы обрабатывают разные экземпляры сервера).
*   **Зависимость от OpenAI:** Мы жестко зависим от OpenAI-совместимого API. Для корпоративных клиентов важно иметь опцию локального или самохостингового LLM.

### 2. Рекомендации по Улучшению (Следующие Шаги)

| Приоритет | Направление | Описание Улучшения |
| :--- | :--- | :--- |
| **Высокий** | **База Знаний (RAG)** | Переход от `knowledge_base.txt` к **векторной базе данных** (например, ChromaDB или Pinecone). Это позволит управлять тысячами документов, обновлять их в реальном времени и сделает RAG-ответы более точными. |
| **Высокий** | **Развертывание** | Использование **Hugging Face Spaces** с `gradio` или `Streamlit` для создания **визуального интерфейса** (Demo Space), чтобы клиенты могли протестировать чат-бота без cURL. |
| **Средний** | **Память (Context)** | Интеграция с **Redis** или другой внешней службой для **хранения истории диалогов**. Это обеспечит настоящую, масштабируемую память, которая не сбрасывается. |
| **Средний** | **Гибкость LLM** | Добавление поддержки **Hugging Face Hub** для использования **Open-Source LLM** (например, Llama 3) вместо коммерческих API. Это снизит зависимость и стоимость. |
| **Низкий** | **Мониторинг** | Внедрение простого логирования и метрик для отслеживания производительности чат-бота (например, время ответа, количество ошибок). |

**Заключение Эксперта:** Мы создали отличный, чистый MVP. Следующий шаг — это **масштабирование базы знаний и памяти**, чтобы перейти от прототипа к корпоративному решению.

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
    ├── chatbot.py            # Core LightRAG RAG and Context Management logic
    └── data/
        └── knowledge_base.txt  # The source of truth for RAG (editable knowledge base)
```
