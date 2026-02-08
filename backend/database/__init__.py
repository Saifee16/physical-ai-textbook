"""
Database package initialization
"""
from .postgres import (
    init_db,
    close_db,
    get_db_session,
    create_user,
    get_user_by_email,
    get_user_profile,
    create_chat_session,
    save_chat_message,
    get_chat_history,
    get_cached_translation,
    cache_translation
)

from .qdrant_client import (
    init_qdrant,
    get_qdrant_client,
    search_vectors,
    upsert_vectors,
    get_collection_info
)

__all__ = [
    # Postgres
    'init_db',
    'close_db',
    'get_db_session',
    'create_user',
    'get_user_by_email',
    'get_user_profile',
    'create_chat_session',
    'save_chat_message',
    'get_chat_history',
    'get_cached_translation',
    'cache_translation',
    
    # Qdrant
    'init_qdrant',
    'get_qdrant_client',
    'search_vectors',
    'upsert_vectors',
    'get_collection_info'
]