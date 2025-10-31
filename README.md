# NovaPay Customer Support AI Agent Platform (Proposal Version)

## 💡 Overview: From Chatbot to AI Agent Platform

Этот репозиторий демонстрирует потенциал роста и развития **NovaPay Customer Support Chatbot** до полноценной **AI Agent Platform**. Мы переходим от простого RAG-чат-бота к модульной архитектуре, способной интегрироваться с передовыми голосовыми AI-сервисами, такими как **Vapi** и **Retell AI**.

**Текущая версия** используется как **Proposal Version** (версия для предложений и рекомендаций). Она показывает модульность ядра и готовность к внедрению современных трендов.

### Key Features & Growth Potential

| Feature | Description | Growth Potential / Trend |
| :--- | :--- | :--- |
| **Modular AI Agent Core** | Основная логика RAG-пайплайна вынесена в отдельный модуль (`src/app.py`), что позволяет легко подключать ее к различным интерфейсам. | **AI Agents:** Готовность к созданию многофункциональных агентов, а не только чат-ботов. |
| **Voice AI Integration Ready** | Архитектура позволяет использовать основной агент для обработки запросов от голосовых AI-сервисов. | **Vapi / Retell AI:** Прямая интеграция с платформами для создания высококачественных голосовых ассистентов, что является ключевым трендом в клиентском сервисе. |
| **Multi-LLM Support** | Динамическое переключение между **OpenAI, Google (Gemini), и Anthropic (Claude)**. | **Flexibility & Cost Optimization:** Выбор лучшей модели для конкретной задачи и бюджета клиента. |
| **Examples & Blueprints** | Добавлена папка `examples/` с примерами интеграций и демонстрационными MVP. | **Rapid Prototyping:** Предоставление клиентам готовых "чертежей" (blueprints) для быстрого запуска. |

---

## 🚀 Quick Start: Demo MVP (Moved to Examples)

Визуальное демо (Streamlit MVP) теперь находится в папке `examples/` и используется исключительно для быстрой демонстрации RAG-логики.

### Запуск Демо

1.  **Клонируйте** репозиторий:
    ```bash
    git clone https://github.com/NovaPay311/customer_support_chatbot.git
    cd customer_support_chatbot
    ```
2.  **Настройте** `.env` (см. `.env.example`).
3.  **Запустите Streamlit Demo** (на порту 8501):
    ```bash
    # Сборка и запуск Docker-контейнера
    docker build -t novapay-agent . && docker run -d -p 8501:8501 --env-file .env --name novapay-agent novapay-agent streamlit run examples/streamlit_demo.py --server.port=8501 --server.address=0.0.0.0
    ```
4.  Откройте в браузере адрес: `http://localhost:8501`

---

## 🛠️ Project Structure (Modular & Future-Proof)

Проект реструктурирован для повышения модульности и демонстрации потенциала роста.

```
.
├── .env.example              # Template for environment variables (API keys, model names, DBs)
├── .dockerignore             # Files to ignore when building Docker image (venv, cache)
├── .gitignore                # Files to ignore (venv, .env, cache)
├── context7.json             # Context7 configuration for documentation indexing
├── Dockerfile                # Docker configuration for Streamlit Demo MVP
├── README.md                 # Project documentation and use cases
├── requirements.txt          # Python dependencies
├── examples/                 # Папка с примерами и демонстрационными MVP
│   ├── streamlit_demo.py     # Визуальное демо (Streamlit MVP)
│   └── vapi_integration_mock.py # Пример интеграции с голосовыми AI (Vapi/Retell AI)
└── src/                      # Основное ядро AI Agent
    ├── __init__.py           # Python package marker
    ├── app.py                # Основной модуль AI Agent (точка входа для Vapi/Retell AI)
    ├── api_flask.py          # Оригинальный Flask API (для интеграции с 1C/Bitrix24)
    ├── chatbot.py            # Core LangChain RAG и Multi-LLM логика
    └── data/
        └── knowledge_base.txt  # Источник знаний для RAG
```

---

## 🗺️ Roadmap: План Дальнейшей Разработки (Next Steps)

Для дальнейшего развития проекта и превращения его в полноценную платформу AI-агентов, предлагается следующий план. (См. файл `ROADMAP.md`)

---
