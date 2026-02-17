"""
Handler Manager
===============

Sistema de gestión de handlers dinámicos.
Carga handlers desde config_handlers.json y los ejecuta según el código.
"""

import json
import os
import importlib
from typing import Dict, Optional, List
from handlers.base_handler import BaseHandler


class HandlerManager:
    """
    Gestiona la carga y ejecución de handlers dinámicamente.
    """
    
    def __init__(self, config_path: str = None):
        """
        Inicializa el gestor de handlers.
        
        Args:
            config_path: Ruta al archivo config_handlers.json
        """
        if config_path is None:
            # Ruta por defecto
            base_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(base_dir, "config_handlers.json")
        
        self.config_path = config_path
        self.handlers_config = {}
        self.handlers_cache = {}  # Cache de instancias de handlers
        
        # Cargar configuración
        self._load_config()
    
    
    def _load_config(self):
        """Carga la configuración de handlers desde JSON"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.handlers_config = json.load(f)
            
            print(f"[HANDLER_MANAGER] Configuración cargada: {len(self.handlers_config)} handlers")
            
            # Mostrar handlers activos
            activos = [codigo for codigo, cfg in self.handlers_config.items() if cfg.get("activo", False)]
            print(f"[HANDLER_MANAGER] Handlers activos: {', '.join(activos)}")
            
        except FileNotFoundError:
            print(f"[HANDLER_MANAGER] ⚠️ No se encontró config_handlers.json en {self.config_path}")
            self.handlers_config = {}
        except json.JSONDecodeError as e:
            print(f"[HANDLER_MANAGER] ❌ Error al parsear JSON: {e}")
            self.handlers_config = {}
    
    
    def get_handler(self, codigo: str) -> Optional[BaseHandler]:
        """
        Obtiene una instancia del handler por su código.
        
        Args:
            codigo: Código del handler (ej: A001, B001)
        
        Returns:
            Instancia del handler o None si no existe
        """
        # Verificar si existe en config
        if codigo not in self.handlers_config:
            print(f"[HANDLER_MANAGER] ⚠️ Handler {codigo} no existe en config")
            return None
        
        config = self.handlers_config[codigo]
        
        # Verificar si está activo
        if not config.get("activo", False):
            print(f"[HANDLER_MANAGER] ⚠️ Handler {codigo} está inactivo")
            return None
        
        # Si ya está en cache, retornar
        if codigo in self.handlers_cache:
            return self.handlers_cache[codigo]
        
        # Cargar handler dinámicamente
        try:
            archivo = config.get("archivo", f"handler_{codigo}.py")
            clase_nombre = config.get("clase", f"Handler{codigo}")
            
            # Importar módulo
            modulo_nombre = archivo.replace(".py", "")
            modulo = importlib.import_module(f"handlers.{modulo_nombre}")
            
            # Obtener clase
            clase = getattr(modulo, clase_nombre)
            
            # Crear instancia
            instancia = clase(codigo=codigo, config=config)
            
            # Guardar en cache
            self.handlers_cache[codigo] = instancia
            
            print(f"[HANDLER_MANAGER] ✓ Handler {codigo} cargado: {config.get('nombre')}")
            
            return instancia
            
        except Exception as e:
            print(f"[HANDLER_MANAGER] ❌ Error cargando handler {codigo}: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    
    def ejecutar_handler(
        self,
        codigo: str,
        from_user: str,
        respuestas: Dict[str, str],
        grupo_id: Optional[str] = None
    ) -> Optional[str]:
        """
        Ejecuta un handler con los datos capturados.
        
        Args:
            codigo: Código del handler
            from_user: Teléfono del usuario
            respuestas: Diccionario con respuestas capturadas
            grupo_id: GUID del grupo (opcional)
        
        Returns:
            Mensaje de respuesta para el usuario o None si hay error
        """
        handler = self.get_handler(codigo)
        
        if not handler:
            return None
        
        try:
            # Determinar grupo_id
            config = self.handlers_config[codigo]
            
            # Si tiene grupo_override, usarlo
            if config.get("grupo_override"):
                grupo_id_final = config["grupo_override"]
                print(f"[HANDLER_MANAGER] Usando grupo_override: {grupo_id_final}")
            elif config.get("usa_grupo_de_dataverse", True):
                grupo_id_final = grupo_id
                print(f"[HANDLER_MANAGER] Usando grupo de Dataverse: {grupo_id_final}")
            else:
                grupo_id_final = None
                print(f"[HANDLER_MANAGER] Sin grupo (handler no requiere grupo)")
            
            # Ejecutar acción final del handler
            mensaje_respuesta = handler.ejecutar_accion_final(
                from_user=from_user,
                respuestas=respuestas,
                grupo_id=grupo_id_final
            )
            
            return mensaje_respuesta
            
        except Exception as e:
            print(f"[HANDLER_MANAGER] ❌ Error ejecutando handler {codigo}: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    
    def get_preguntas(self, codigo: str) -> List[str]:
        """
        Obtiene las preguntas de un handler.
        
        Args:
            codigo: Código del handler
        
        Returns:
            Lista de preguntas o lista vacía si hay error
        """
        handler = self.get_handler(codigo)
        
        if not handler:
            return []
        
        try:
            return handler.get_preguntas()
        except Exception as e:
            print(f"[HANDLER_MANAGER] ❌ Error obteniendo preguntas de {codigo}: {e}")
            return []
    
    
    def handler_existe(self, codigo: str) -> bool:
        """
        Verifica si un handler existe y está activo.
        
        Args:
            codigo: Código del handler
        
        Returns:
            True si existe y está activo
        """
        if codigo not in self.handlers_config:
            return False
        
        return self.handlers_config[codigo].get("activo", False)
    
    
    def listar_handlers_activos(self) -> Dict[str, Dict]:
        """
        Retorna diccionario con todos los handlers activos.
        
        Returns:
            Dict con código -> config de handlers activos
        """
        return {
            codigo: config 
            for codigo, config in self.handlers_config.items() 
            if config.get("activo", False)
        }
    
    
    def reload_config(self):
        """Recarga la configuración desde el archivo JSON"""
        self.handlers_cache.clear()
        self._load_config()
        print("[HANDLER_MANAGER] Configuración recargada")


# Instancia global del gestor
_handler_manager = None


def get_handler_manager() -> HandlerManager:
    """
    Obtiene la instancia singleton del HandlerManager.
    
    Returns:
        Instancia global de HandlerManager
    """
    global _handler_manager
    
    if _handler_manager is None:
        _handler_manager = HandlerManager()
    
    return _handler_manager
