#!/usr/bin/env python3
"""Verify Qdrant connection and collection"""
import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from database.qdrant_client import init_qdrant, get_collection_info

async def main():
    print("=" * 60)
    print("Verifying Qdrant Setup")
    print("=" * 60)
    
    try:
        await init_qdrant()
        info = get_collection_info()
        
        print(f"\\n✅ Qdrant Connected!")
        print(f"Collection: {info['name']}")
        print(f"Vectors: {info['points_count']}")
        print(f"Status: {info['status']}")
    except Exception as e:
        print(f"\\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())