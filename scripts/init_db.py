#!/usr/bin/env python3
"""Initialize database with tables"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from database.postgres import init_db, create_tables

async def main():
    print("=" * 60)
    print("Initializing Database")
    print("=" * 60)
    
    try:
        await init_db()
        print("\\n✅ Database initialized successfully!")
    except Exception as e:
        print(f"\\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())