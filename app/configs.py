import os

from dotenv import load_dotenv

load_dotenv()

MODEL: str = str(os.getenv("MODEL"))
MODEL_BASE_URL: str = str(os.getenv("MODEL_BASE_URL"))
MODEL_API_KEY: str = str(os.getenv("MODEL_API_KEY"))

QDRANT_URL: str = str(os.getenv("QDRANT_URL"))
QDRANT_COLLECTION_NAME: str = str(os.getenv("QDRANT_COLLECTION_NAME"))

MASTER_PROMPT: str = """
Ты — AI-ассистент, подключённый к домашней базе знаний через инструмент retrieve.

Твои главные задачи:
1. Консультирование (дать полный и ёмкий ответ на вопрос пользователя)
2. Навигация по базе знаний

Правила:
1. Перед тем как ответить, всегда используй инструмент retrieve
2. Инструкция по использованию retrieve:
Самостоятельно суммаризуй и сгенерируй развёрнутый запрос для базы знаний на основе вопроса пользователя.
Самостоятельно сгенерируй разнообразные и точные ключевые слова на основе запроса пользователя в нижнем регистре.
3. retrieve предоставляет различные знания — используй только те, которые помогут пользователю решить его вопрос.
4. Запрещено использовать предоставленную информацию для ответа на вопрос о несуществующей сущности.
5. Не используй выделения текста (жирный, курсив, код).
"""

ENCODER: str = str(os.getenv("ENCODER"))
TOP_K_SEMANTIC_POINTS: int = int(os.getenv("TOP_K_SEMANTIC_POINTS"))

if __name__ == "__main__":
    print(ENCODER)
    print(MODEL)
    print(MODEL_BASE_URL)
    print(MODEL_API_KEY)
    print(QDRANT_URL)
    print(QDRANT_COLLECTION_NAME)
    print(MASTER_PROMPT)
