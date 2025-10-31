# src/app.py
# Основной модуль для запуска AI Agent.
# Этот файл будет служить точкой входа для будущей интеграции с Vapi, Retell AI или другими платформами.

import os
from .chatbot import Chatbot

# Инициализация основного агента
class AIAgent:
    def __init__(self):
        # Здесь будет логика загрузки конфигурации, LLM, и RAG-пайплайна
        self.chatbot = Chatbot()
        print("AI Agent initialized and ready for action.")

    def process_request(self, input_data: str):
        # Основная логика обработки запроса (текст, голос, API)
        response = self.chatbot.get_response(input_data)
        return {"response": response, "agent_status": "processed"}

# Заглушка для демонстрации
if __name__ == "__main__":
    agent = AIAgent()
    test_query = "What is the main feature of this project?"
    result = agent.process_request(test_query)
    print(f"Test Query: {test_query}")
    print(f"Agent Response: {result['response']}")
    print(f"Agent Status: {result['agent_status']}")
