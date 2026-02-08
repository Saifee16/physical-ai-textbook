#!/usr/bin/env python3
"""Test all connections"""
import asyncio
import sys
from pathlib import Path
import os

sys.path.append(str(Path(__file__).parent.parent))

from database.postgres import init_db
from database.qdrant_client import init_qdrant
from services.openai_service import openai_service

async def main():
    print("=" * 60)
    print("Testing All Connections")
    print("=" * 60)
    
    # Test Postgres
    print("\\n1. Testing Neon Postgres...")
    try:
        await init_db()
        print("   ✅ Postgres connected")
    except Exception as e:
        print(f"   ❌ Postgres failed: {e}")
    
    # Test Qdrant
    print("\\n2. Testing Qdrant...")
    try:
        await init_qdrant()
        print("   ✅ Qdrant connected")
    except Exception as e:
        print(f"   ❌ Qdrant failed: {e}")
    
    # Test OpenAI
    print("\\n3. Testing OpenAI...")
    try:
        embedding = openai_service.generate_embedding("test")
        print(f"   ✅ OpenAI connected (embedding size: {len(embedding)})")
    except Exception as e:
        print(f"   ❌ OpenAI failed: {e}")
    
    print("\\n" + "=" * 60)
    print("Connection test complete!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())