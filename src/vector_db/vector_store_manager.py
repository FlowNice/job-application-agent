import logging
from typing import List, Dict, Optional
import numpy as np

logger = logging.getLogger(__name__)

class VectorStoreManager:
    """
    Manages the vector database for storing and searching embeddings of vacancies and resumes.
    
    This implementation uses a simple in-memory list as a placeholder for a real 
    vector database like Pinecone, Weaviate, or pgvector (PostgreSQL).
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.store = [] # Placeholder for vector store: list of {"id": str, "vector": np.array, "metadata": Dict}
        self.embedding_dimension = 768 # Предполагаемая размерность эмбеддинга
        logger.info("VectorStoreManager initialized. Using in-memory store.")

    def _generate_embedding(self, text: str) -> np.ndarray:
        """
        Placeholder для генерации эмбеддинга текста.
        В реальной реализации будет использоваться LLM-клиент.
        """
        # Временная заглушка: возвращает случайный вектор
        logger.debug(f"Generating mock embedding for text: {text[:30]}...")
        return np.random.rand(self.embedding_dimension)

    def add_vacancy_vector(self, vacancy_id: str, text_to_embed: str, metadata: Dict) -> None:
        """
        Генерирует эмбеддинг для вакансии и добавляет его в хранилище.
        """
        vector = self._generate_embedding(text_to_embed)
        self.store.append({
            "id": vacancy_id,
            "vector": vector,
            "metadata": metadata
        })
        logger.info(f"Added vector for vacancy ID: {vacancy_id}. Total vectors: {len(self.store)}")

    def search_similar_vacancies(self, query_text: str, top_k: int = 5) -> List[Dict]:
        """
        Ищет наиболее похожие вакансии на основе текстового запроса.
        """
        query_vector = self._generate_embedding(query_text)
        
        # Временная заглушка: расчет косинусного сходства (cosine similarity)
        results = []
        for item in self.store:
            # Расчет сходства (dot product для нормализованных векторов)
            similarity = np.dot(query_vector, item["vector"]) / (np.linalg.norm(query_vector) * np.linalg.norm(item["vector"]))
            results.append({
                "id": item["id"],
                "similarity": similarity,
                "metadata": item["metadata"]
            })
            
        # Сортировка по сходству и выбор top_k
        results.sort(key=lambda x: x["similarity"], reverse=True)
        
        logger.info(f"Search completed. Found {len(results)} results, returning top {top_k}.")
        return results[:top_k]

    def get_vector_by_id(self, vacancy_id: str) -> Optional[Dict]:
        """
        Получает вектор и метаданные по ID.
        """
        for item in self.store:
            if item["id"] == vacancy_id:
                return item
        return None

if __name__ == "__main__":
    # Пример использования (Example usage)
    manager = VectorStoreManager({})
    
    # Добавление векторов
    manager.add_vacancy_vector(
        "v1", 
        "Senior Python Developer with Django and PostgreSQL experience.", 
        {"title": "Python Dev", "company": "A"}
    )
    manager.add_vacancy_vector(
        "v2", 
        "Junior Frontend Developer using React and TypeScript.", 
        {"title": "Frontend Dev", "company": "B"}
    )
    manager.add_vacancy_vector(
        "v3", 
        "Lead Backend Engineer, strong in Python, FastAPI, and AWS.", 
        {"title": "Lead Backend", "company": "C"}
    )
    
    # Поиск
    query = "I am looking for a Python backend job."
    results = manager.search_similar_vacancies(query, top_k=2)
    
    print(f"\nSearch Query: {query}")
    for result in results:
        print(f"ID: {result['id']}, Similarity: {result['similarity']:.4f}, Title: {result['metadata']['title']}")

