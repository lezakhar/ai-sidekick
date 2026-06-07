from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

from langchain.tools import tool

import configs


try:
    encoder = SentenceTransformer(configs.ENCODER)
    encoder.encode("test")
except Exception as e:
    print(f"Failed to load encoder: {e}")
    raise e


qdrant_client = QdrantClient(
    url=configs.QDRANT_URL,
    port=None,
)


def search_points(
    user_query: str,
    keywords: list[str],
    encoder: SentenceTransformer,
) -> list:
    encoded_query = encoder.encode(
        user_query,
        normalize_embeddings=True,
    ).tolist()

    top_k_points = []

    try:
        top_k_points = qdrant_client.query_points(
            collection_name=configs.QDRANT_COLLECTION_NAME,
            query=encoded_query,
            limit=configs.TOP_K_SEMANTIC_POINTS,
            with_payload=True,
            score_threshold=0.4,
        ).points
    except Exception as e:
        print(e)

    boost_factor = 0.05
    keywords_set: set = set(keywords)
    for point in top_k_points:
        point_kw = set(point.payload["keywords"])
        point.score += boost_factor * len(keywords_set.intersection(point_kw))

    return sorted(top_k_points, key=lambda x: x.score, reverse=True)[:2]


@tool(response_format="content_and_artifact")
def retrieve(
    user_query: str,
    keywords: list[str],
) -> tuple[str, list[int]]:
    """Получить информацию из векторной базы знаний
    Args:
        user_query: Запрос пользователя (строка str)
            Пример: Где я сохранил контакты сантехника?
        keywords: Ключевые слова для лексического поиска, без лишних escape-символов (список строк)
            Пример: ["сантехник", "водопровод", "ремонт", "контакты", "мастер"]
    Returns:
        str: Сформированный контекст из Базы знаний
        list[int]: Идентификаторы документов из Базы знаний (на основе которых сформирован контекст)
    Note:
        LLM Необходимо самостоятельно на русском языке отредактировать запрос пользователя
        и сформировать список ключевых слов на русском языке перед вызовом метода.
    """
    top_points = search_points(
        user_query=user_query,
        keywords=keywords,
        encoder=encoder,
    )

    
    if not top_points:
        return "Релевантные знания отсутствуют", []

    context = "Найденные знания:" + "\n"
    retrieved_docs: list = []
    for point in top_points:
        payload = point.payload

        title = str(payload.get("title", ""))
        text = str(payload.get("text", ""))
        source_file = str(payload.get("source_file", ""))

        knowledge = f"source_file: {source_file}\ntitle: {title}\ntext: {text}\n"
        context += knowledge

        retrieved_docs.append(point.id)

    return context, retrieved_docs
