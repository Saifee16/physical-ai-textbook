"""
Qdrant Vector Database Client
"""
import os
from typing import List, Dict, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
import logging

logger = logging.getLogger(__name__)

# Global Qdrant client
_client: Optional[QdrantClient] = None
COLLECTION_NAME = "physical_ai_textbook"

async def init_qdrant():
    """Initialize Qdrant client"""
    global _client
    
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    
    if not qdrant_url or not qdrant_api_key:
        raise ValueError("QDRANT_URL or QDRANT_API_KEY not set")
    
    try:
        _client = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key,
            timeout=60
        )
        
        # Verify connection
        collections = _client.get_collections()
        logger.info(f"✅ Connected to Qdrant. Collections: {len(collections.collections)}")
        
        # Create collection if it doesn't exist
        await create_collection_if_not_exists()
        
    except Exception as e:
        logger.error(f"Failed to connect to Qdrant: {e}")
        raise

async def create_collection_if_not_exists():
    """Create collection if it doesn't exist"""
    try:
        collections = _client.get_collections().collections
        collection_names = [c.name for c in collections]
        
        if COLLECTION_NAME not in collection_names:
            _client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=1536,  # text-embedding-3-small dimension
                    distance=Distance.COSINE
                )
            )
            logger.info(f"✅ Created collection: {COLLECTION_NAME}")
        else:
            logger.info(f"Collection '{COLLECTION_NAME}' already exists")
    
    except Exception as e:
        logger.error(f"Error creating collection: {e}")

def get_qdrant_client() -> QdrantClient:
    """Get Qdrant client instance"""
    if not _client:
        raise RuntimeError("Qdrant client not initialized. Call init_qdrant() first")
    return _client

def search_vectors(
    query_vector: List[float],
    limit: int = 5,
    score_threshold: float = 0.7,
    chapter_filter: Optional[str] = None
) -> List[Dict]:
    """Search for similar vectors in Qdrant"""
    search_filter = None
    
    if chapter_filter:
        search_filter = Filter(
            must=[
                FieldCondition(
                    key="chapter",
                    match=MatchValue(value=chapter_filter)
                )
            ]
        )
    
    results = _client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=limit,
        score_threshold=score_threshold,
        query_filter=search_filter
    )
    
    return [
        {
            "text": result.payload.get("text", ""),
            "chapter": result.payload.get("chapter", ""),
            "section": result.payload.get("section", ""),
            "title": result.payload.get("title", ""),
            "score": result.score
        }
        for result in results
    ]

def upsert_vectors(points: List[PointStruct]):
    """Upsert vectors into Qdrant"""
    _client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

def get_collection_info() -> Dict:
    """Get collection information"""
    info = _client.get_collection(COLLECTION_NAME)
    return {
        "name": COLLECTION_NAME,
        "points_count": info.points_count,
        "vectors_count": info.vectors_count,
        "status": info.status
    }