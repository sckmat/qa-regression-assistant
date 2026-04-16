from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):
    """
    Абстрактный провайдер embeddings.

    На вход принимает список текстов.
    На выходе возвращает список векторов.
    """

    @abstractmethod
    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError