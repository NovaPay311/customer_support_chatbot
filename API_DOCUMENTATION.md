# REST API Documentation

## Обзор

REST API предоставляет унифицированный интерфейс для взаимодействия с чат-ботом поддержки клиентов NovaPay. API построен на базе **FastAPI** и поддерживает сессионность, отслеживание пользователей и историю разговоров.

## Базовая информация

- **Базовый URL:** `http://localhost:8000` (по умолчанию)
- **Версия API:** 1.0.0
- **Формат данных:** JSON
- **Аутентификация:** Не требуется (для MVP)

## Основные эндпоинты

### 1. Запрос к чат-боту

**Endpoint:** `POST /api/v1/query`

**Описание:** Отправить вопрос чат-боту и получить ответ.

**Request Body:**
```json
{
  "query": "Какие комиссии за переводы?",
  "session_id": "optional-session-id",
  "user_id": "optional-user-id",
  "metadata": {
    "language": "ru",
    "source": "web"
  }
}
```

**Response (200 OK):**
```json
{
  "query_id": "550e8400-e29b-41d4-a716-446655440000",
  "session_id": "550e8400-e29b-41d4-a716-446655440001",
  "query": "Какие комиссии за переводы?",
  "response": "Комиссии за переводы зависят от типа перевода...",
  "confidence": null,
  "source_documents": null,
  "timestamp": "2025-11-03T12:00:00",
  "processing_time_ms": 250.5
}
```

**Параметры:**
- `query` (обязательно): Вопрос пользователя (1-1000 символов)
- `session_id` (опционально): ID сессии для сохранения контекста разговора
- `user_id` (опционально): ID пользователя для отслеживания
- `metadata` (опционально): Дополнительные метаданные

**Коды ошибок:**
- `400`: Неверный запрос (отсутствует `query`)
- `503`: Сервис недоступен (чат-бот не инициализирован)
- `500`: Внутренняя ошибка сервера

---

### 2. Создание новой сессии

**Endpoint:** `POST /api/v1/session`

**Описание:** Создать новую сессию для начала разговора.

**Query Parameters:**
- `user_id` (опционально): ID пользователя

**Response (200 OK):**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440001",
  "created_at": "2025-11-03T12:00:00"
}
```

---

### 3. Получение истории сессии

**Endpoint:** `GET /api/v1/session/{session_id}`

**Описание:** Получить историю разговора для конкретной сессии.

**Path Parameters:**
- `session_id` (обязательно): ID сессии

**Response (200 OK):**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440001",
  "user_id": "user-123",
  "created_at": "2025-11-03T12:00:00",
  "conversation_history": [
    {
      "query": "Какие комиссии за переводы?",
      "response": "Комиссии за переводы зависят от типа перевода...",
      "timestamp": "2025-11-03T12:00:00"
    },
    {
      "query": "А какой лимит?",
      "response": "Лимит зависит от статуса аккаунта...",
      "timestamp": "2025-11-03T12:01:00"
    }
  ]
}
```

**Коды ошибок:**
- `404`: Сессия не найдена

---

### 4. Проверка здоровья сервиса

**Endpoint:** `GET /health`

**Описание:** Проверить статус сервиса и доступность чат-бота.

**Response (200 OK):**
```json
{
  "status": "ok",
  "service": "NovaPay Chatbot API",
  "timestamp": "2025-11-03T12:00:00"
}
```

**Возможные статусы:**
- `ok`: Все компоненты работают нормально
- `degraded`: Чат-бот недоступен, но API работает

---

### 5. Информация об API

**Endpoint:** `GET /`

**Описание:** Получить основную информацию об API.

**Response (200 OK):**
```json
{
  "service": "NovaPay Customer Support Chatbot API",
  "version": "1.0.0",
  "docs": "/docs",
  "openapi": "/openapi.json"
}
```

---

## Примеры использования

### cURL

**Запрос к чат-боту:**
```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Как создать аккаунт?",
    "user_id": "user-123"
  }'
```

**Создание новой сессии:**
```bash
curl -X POST "http://localhost:8000/api/v1/session?user_id=user-123"
```

**Получение истории сессии:**
```bash
curl -X GET "http://localhost:8000/api/v1/session/550e8400-e29b-41d4-a716-446655440001"
```

### Python

```python
import requests

# Создание сессии
session_response = requests.post("http://localhost:8000/api/v1/session", params={"user_id": "user-123"})
session_id = session_response.json()["session_id"]

# Запрос к чат-боту
query_response = requests.post(
    "http://localhost:8000/api/v1/query",
    json={
        "query": "Как создать аккаунт?",
        "session_id": session_id,
        "user_id": "user-123"
    }
)

print(query_response.json()["response"])
```

### JavaScript/Node.js

```javascript
// Создание сессии
const sessionResponse = await fetch("http://localhost:8000/api/v1/session?user_id=user-123", {
  method: "POST"
});
const { session_id } = await sessionResponse.json();

// Запрос к чат-боту
const queryResponse = await fetch("http://localhost:8000/api/v1/query", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    query: "Как создать аккаунт?",
    session_id: session_id,
    user_id: "user-123"
  })
});

const data = await queryResponse.json();
console.log(data.response);
```

---

## Интерактивная документация

FastAPI автоматически генерирует интерактивную документацию:

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
- **OpenAPI Schema:** `http://localhost:8000/openapi.json`

---

## Запуск API

### С использованием Uvicorn

```bash
uvicorn src.api_fastapi:app --host 0.0.0.0 --port 8000 --reload
```

### С использованием Docker

```bash
docker build -t novapay-chatbot .
docker run -p 8000:8000 novapay-chatbot
```

---

## Лучшие практики

1. **Используйте сессии:** Сохраняйте `session_id` для сохранения контекста разговора между запросами.
2. **Обрабатывайте ошибки:** Всегда проверяйте статус HTTP ответа и обрабатывайте ошибки.
3. **Логирование:** Используйте `query_id` для отслеживания запросов в логах.
4. **Кэширование:** Кэшируйте часто задаваемые вопросы на клиентской стороне для улучшения производительности.
5. **Таймауты:** Установите таймауты для запросов (рекомендуется 30 секунд).

---

## Будущие улучшения

- Аутентификация и авторизация (OAuth 2.0, API ключи)
- Ограничение частоты запросов (Rate Limiting)
- Кэширование ответов (Redis)
- Метрики и мониторинг (Prometheus)
- WebSocket поддержка для real-time общения
- Интеграция с внешними сервисами (CRM, Zendesk)
