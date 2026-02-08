"""
Neon Postgres Database Connection and Operations
"""
import os
from typing import List, Dict, Optional
import asyncpg
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Database connection pool
_pool: Optional[asyncpg.Pool] = None

async def init_db():
    """Initialize database connection pool"""
    global _pool
    
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL not set in environment")
    
    try:
        _pool = await asyncpg.create_pool(
            database_url,
            min_size=2,
            max_size=10,
            command_timeout=60
        )
        logger.info("✅ Connected to Neon Postgres")
        
        # Create tables if they don't exist
        await create_tables()
        
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        raise

async def create_tables():
    """Create all database tables"""
    async with _pool.acquire() as conn:
        # Users table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW()
            )
        """)
        
        # User profiles table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS user_profiles (
                user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
                software_level VARCHAR(50),
                hardware_level VARCHAR(50),
                robotics_knowledge BOOLEAN DEFAULT FALSE,
                learning_goals TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        
        # Chat sessions table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS chat_sessions (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                user_id UUID REFERENCES users(id) ON DELETE SET NULL,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        
        # Chat messages table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS chat_messages (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                session_id UUID REFERENCES chat_sessions(id) ON DELETE CASCADE,
                role VARCHAR(20) NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        
        # Translation cache table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS translation_cache (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                chapter_id VARCHAR(255) NOT NULL,
                source_content_hash VARCHAR(64) NOT NULL,
                translated_content TEXT NOT NULL,
                target_language VARCHAR(10) NOT NULL,
                created_at TIMESTAMP DEFAULT NOW(),
                UNIQUE(chapter_id, source_content_hash, target_language)
            )
        """)
        
        logger.info("✅ Database tables created/verified")

async def get_db_session():
    """Get database connection from pool"""
    if not _pool:
        await init_db()
    return _pool

async def close_db():
    """Close database connection pool"""
    global _pool
    if _pool:
        await _pool.close()
        logger.info("Database connection closed")

# User operations
async def create_user(email: str, password_hash: str, profile: Dict) -> str:
    """Create a new user with profile"""
    async with _pool.acquire() as conn:
        async with conn.transaction():
            # Create user
            user_id = await conn.fetchval(
                "INSERT INTO users (email, password_hash) VALUES ($1, $2) RETURNING id",
                email, password_hash
            )
            
            # Create profile
            await conn.execute("""
                INSERT INTO user_profiles (user_id, software_level, hardware_level, robotics_knowledge, learning_goals)
                VALUES ($1, $2, $3, $4, $5)
            """, user_id, profile.get('software_level'), profile.get('hardware_level'), 
               profile.get('robotics_knowledge', False), profile.get('learning_goals'))
            
            return str(user_id)

async def get_user_by_email(email: str) -> Optional[Dict]:
    """Get user by email"""
    async with _pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM users WHERE email = $1",
            email
        )
        return dict(row) if row else None

async def get_user_profile(user_id: str) -> Optional[Dict]:
    """Get user profile"""
    async with _pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM user_profiles WHERE user_id = $1",
            user_id
        )
        return dict(row) if row else None

# Chat operations
async def create_chat_session(user_id: Optional[str] = None) -> str:
    """Create a new chat session"""
    async with _pool.acquire() as conn:
        session_id = await conn.fetchval(
            "INSERT INTO chat_sessions (user_id) VALUES ($1) RETURNING id",
            user_id
        )
        return str(session_id)

async def save_chat_message(session_id: str, user_id: Optional[str], role: str, content: str):
    """Save a chat message"""
    async with _pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO chat_messages (session_id, role, content)
            VALUES ($1, $2, $3)
        """, session_id, role, content)

async def get_chat_history(session_id: str, limit: int = 20) -> List[Dict]:
    """Get chat history for a session"""
    async with _pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT role, content, created_at
            FROM chat_messages
            WHERE session_id = $1
            ORDER BY created_at DESC
            LIMIT $2
        """, session_id, limit)
        
        # Reverse to get chronological order
        return [dict(row) for row in reversed(rows)]

# Translation cache operations
async def get_cached_translation(chapter_id: str, content_hash: str, target_lang: str) -> Optional[str]:
    """Get cached translation"""
    async with _pool.acquire() as conn:
        row = await conn.fetchrow("""
            SELECT translated_content
            FROM translation_cache
            WHERE chapter_id = $1 AND source_content_hash = $2 AND target_language = $3
        """, chapter_id, content_hash, target_lang)
        
        return row['translated_content'] if row else None

async def cache_translation(chapter_id: str, content_hash: str, target_lang: str, translated_content: str):
    """Cache a translation"""
    async with _pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO translation_cache (chapter_id, source_content_hash, target_language, translated_content)
            VALUES ($1, $2, $3, $4)
            ON CONFLICT (chapter_id, source_content_hash, target_language)
            DO UPDATE SET translated_content = $4
        """, chapter_id, content_hash, target_lang, translated_content)