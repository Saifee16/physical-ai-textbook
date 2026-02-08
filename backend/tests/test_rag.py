import pytest
from services.rag_service import rag_service

@pytest.mark.asyncio
async def test_embedding_generation():
    text = "Test text for embedding"
    embedding = await rag_service.embed_text(text)
    assert len(embedding) == 1536  # text-embedding-3-small dimension

@pytest.mark.asyncio
async def test_search():
    chunks = await rag_service.search_similar_chunks("What is ROS 2?")
    assert isinstance(chunks, list)