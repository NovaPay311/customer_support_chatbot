import os
import logging
from typing import List, Dict, Any

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.retrievers import EnsembleRetriever
from langchain.retrievers.document_compressors import HypotheticalDocumentEmbedder
from langchain_core.documents import Document
from langchain_core.language_models import BaseLanguageModel
from langchain_core.vectorstores import VectorStoreRetriever

logger = logging.getLogger(__name__)

# ============================================================================
# HyDE (Hypothetical Document Embedding)
# ============================================================================

def get_hyde_retriever(
    llm: BaseLanguageModel,
    base_retriever: VectorStoreRetriever,
    embedding_model: Any,
) -> HypotheticalDocumentEmbedder:
    """
    Создает ретривер HyDE (Hypothetical Document Embedding).
    
    HyDE генерирует гипотетический ответ на запрос, векторизует его и использует
    для поиска в векторной базе данных.
    """
    logger.info("Setting up HyDE Retriever...")
    
    # Промпт для генерации гипотетического ответа
    HYDE_PROMPT = PromptTemplate(
        input_variables=["question"],
        template="""Вы — эксперт по поддержке клиентов. Ваша задача — сгенерировать
        подробный, но гипотетический ответ на следующий вопрос. Не используйте
        внешние знания, только ваше внутреннее представление о том, как должен
        выглядеть идеальный ответ.

        Вопрос: {question}

        Гипотетический ответ:""",
    )

    # Создание цепочки для генерации гипотетического ответа
    hyde_chain = LLMChain(llm=llm, prompt=HYDE_PROMPT)

    # Создание HyDE-ретривера
    hyde_retriever = HypotheticalDocumentEmbedder(
        llm_chain=hyde_chain,
        base_embeddings=embedding_model,
        base_retriever=base_retriever,
    )
    
    return hyde_retriever

# ============================================================================
# RAG-Fusion (Reciprocal Rank Fusion)
# ============================================================================

def reciprocal_rank_fusion(
    results: List[List[Document]], k: int = 60
) -> List[Document]:
    """
    Объединяет результаты поиска из нескольких запросов с помощью RRF.
    
    Args:
        results: Список списков документов, где каждый внутренний список -
                 результат одного поискового запроса.
        k: Константа для RRF.
        
    Returns:
        Список документов, ранжированных по RRF.
    """
    fused_scores: Dict[str, float] = {}
    
    # 1. Сбор всех документов и расчет RRF
    for rank_list in results:
        for rank, doc in enumerate(rank_list):
            doc_str = doc.page_content
            
            # Используем контент документа как ключ для уникальности
            if doc_str not in fused_scores:
                fused_scores[doc_str] = 0.0
            
            # RRF формула: 1 / (rank + k)
            fused_scores[doc_str] += 1 / (rank + k)

    # 2. Сортировка по fused_scores
    sorted_results = sorted(
        fused_scores.items(), key=lambda x: x[1], reverse=True
    )
    
    # 3. Восстановление объектов Document (для простоты возвращаем только контент)
    # В реальной реализации нужно сохранять метаданные
    final_documents = [
        Document(page_content=content, metadata={"score": score})
        for content, score in sorted_results
    ]
    
    return final_documents

def get_rag_fusion_retriever(
    llm: BaseLanguageModel,
    base_retriever: VectorStoreRetriever,
    k_queries: int = 4,
) -> EnsembleRetriever:
    """
    Создает ретривер RAG-Fusion.
    
    RAG-Fusion генерирует несколько вариантов запроса, выполняет поиск по каждому
    и объединяет результаты с помощью RRF.
    """
    logger.info("Setting up RAG-Fusion Retriever...")
    
    # Промпт для генерации вариантов запроса
    QUERY_PROMPT = PromptTemplate(
        input_variables=["question"],
        template="""Вы — генератор поисковых запросов. Ваша задача —
        сгенерировать {k_queries} разнообразных поисковых запросов, которые
        наилучшим образом отражают суть следующего вопроса.

        Вопрос: {question}

        Сгенерированные запросы (каждый с новой строки):""",
    )
    
    # 1. Цепочка для генерации запросов
    query_chain = LLMChain(llm=llm, prompt=QUERY_PROMPT)
    
    # 2. Функция для выполнения RAG-Fusion
    def rag_fusion_search(question: str) -> List[Document]:
        # Генерация запросов
        response = query_chain.run(question=question, k_queries=k_queries)
        queries = [q.strip() for q in response.split('\n') if q.strip()]
        
        logger.info(f"Generated queries for RAG-Fusion: {queries}")
        
        # Параллельный поиск
        all_results = []
        for q in queries:
            # Используем базовый ретривер для каждого запроса
            results = base_retriever.get_relevant_documents(q)
            all_results.append(results)
            
        # Объединение с помощью RRF
        fused_docs = reciprocal_rank_fusion(all_results)
        
        return fused_docs

    # В LangChain нет прямого "RAG-Fusion Retriever", поэтому мы возвращаем
    # функцию, которую можно использовать как ретривер.
    # Для интеграции в ConversationalRetrievalChain потребуется обертка.
    
    # В качестве упрощения для LangChain, мы можем использовать EnsembleRetriever
    # если бы у нас было несколько разных ретриверов, но для RAG-Fusion
    # нам нужна кастомная логика.
    
    # Для простоты интеграции в текущий код, мы вернем функцию, которую
    # можно использовать напрямую.
    return rag_fusion_search
