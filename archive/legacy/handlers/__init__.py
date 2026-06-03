"""
Handler __init__.py
===================

Módulo para importar handlers fácilmente.
"""

from handlers.base_handler import BaseHandler
from handlers.handler_manager import HandlerManager, get_handler_manager

__all__ = ["BaseHandler", "HandlerManager", "get_handler_manager"]
