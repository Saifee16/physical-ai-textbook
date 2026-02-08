"""
Routes package initialization
"""
from .auth import router as auth_router
from .chat import router as chat_router
from .personalize import router as personalize_router
from .translate import router as translate_router

__all__ = [
    'auth_router',
    'chat_router',
    'personalize_router',
    'translate_router'
]