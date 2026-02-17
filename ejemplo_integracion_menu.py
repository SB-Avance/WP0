"""
EJEMPLO DE INTEGRACIÓN DEL SISTEMA DE MENÚ CONFIABLE
====================================================

Este archivo muestra cómo integrar el sistema de menú confiable
con el backend de Flask existente.
"""
import sys
sys.path.append('backend')
from sistema_menu_confiable import SistemaMenuConfiable, crear_sistema_menu, MenuConfig


# ============================================================================
# INTEGRACIÓN CON FLASK BACKEND
# ============================================================================

class IntegracionMenuWhatsApp:
    """
    Integra el sistema de menú confiable con el webhook de WhatsApp
    """
    
    def __init__(self, sistema_menu: SistemaMenuConfiable):
        """
        Args:
            sistema_menu: Instancia de SistemaMenuConfiable
        """
        self.menu = sistema_menu
    
    def procesar_mensaje_usuario(self, mensaje: str, telefono: str) -> dict:
        """
        Procesa un mensaje del usuario y determina la respuesta
        
        Args:
            mensaje: Texto del mensaje del usuario
            telefono: Número de teléfono del usuario
            
        Returns:
            Dict con la respuesta a enviar
        """
        mensaje_lower = mensaje.lower().strip()
        
        # Caso 1: Usuario pide el menú
        if mensaje_lower in ["menu", "menú", "opciones", "hola", "hi"]:
            return {
                "tipo": "menu",
                "texto": self.menu.obtener_menu_texto()
            }
        
        # Caso 2: Usuario selecciona una opción
        opcion = self.menu.validar_seleccion(mensaje)
        
        if opcion:
            return {
                "tipo": "seleccion_valida",
                "opcion": opcion.to_dict(),
                "texto": f"Ha seleccionado: {opcion.texto}\n\nUn agente se comunicará con usted pronto."
            }
        
        # Caso 3: Mensaje no reconocido
        return {
            "tipo": "no_reconocido",
            "texto": "No entendí su mensaje. Escriba 'MENU' para ver las opciones disponibles."
        }


# ============================================================================
# EJEMPLO EN WEBHOOK DE FLASK
# ============================================================================

# Esto sería en tu archivo principal del backend (ej: app.py)

"""
from flask import Flask, request, jsonify
from sistema_menu_confiable import crear_sistema_menu
from ejemplo_integracion_menu import IntegracionMenuWhatsApp

app = Flask(__name__)

# Inicializar sistema de menú (una sola vez al iniciar la app)
sistema_menu = crear_sistema_menu(DATAVERSE_URL, get_token)
integracion = IntegracionMenuWhatsApp(sistema_menu)

@app.route('/webhook', methods=['POST'])
def webhook():
    '''Webhook de WhatsApp'''
    data = request.get_json()
    
    # Extraer datos del mensaje
    mensaje_info = extraer_mensaje(data)  # Tu función existente
    
    if not mensaje_info:
        return jsonify({"status": "ok"}), 200
    
    telefono = mensaje_info['telefono']
    mensaje = mensaje_info['texto']
    
    # Procesar con el sistema de menú
    respuesta = integracion.procesar_mensaje_usuario(mensaje, telefono)
    
    # Enviar respuesta por WhatsApp
    enviar_whatsapp(telefono, respuesta['texto'])  # Tu función existente
    
    # Guardar en BD si es necesario
    if respuesta['tipo'] == 'seleccion_valida':
        opcion = respuesta['opcion']
        # Asignar conversación al grupo correspondiente
        asignar_grupo(telefono, opcion['categoria'])
    
    return jsonify({"status": "ok"}), 200
"""


# ============================================================================
# CONFIGURACIÓN AVANZADA
# ============================================================================

def configurar_menu_personalizado():
    """
    Ejemplo de cómo personalizar la configuración del menú
    """
    # Cambiar duración del cache
    MenuConfig.CACHE_DURATION_MINUTES = 10  # 10 minutos en vez de 5
    
    # Cambiar mensaje de bienvenida
    MenuConfig.MENSAJE_BIENVENIDA = "🙌 ¡Hola! Seleccione una opción para continuar:"
    
    # Cambiar máximo de opciones
    MenuConfig.MAX_OPCIONES_POR_CATEGORIA = 15
    
    # Deshabilitar logs detallados
    MenuConfig.SHOW_LOGS = False


# ============================================================================
# PRUEBA RÁPIDA
# ============================================================================

if __name__ == "__main__":
    """
    Prueba rápida de la integración
    """
    try:
        from goot import DATAVERSE_URL, CLIENT_ID, CLIENT_SECRET, TENANT_ID
        import requests
        
        def get_token():
            url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
            data = {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "scope": f"{DATAVERSE_URL}/.default",
                "grant_type": "client_credentials"
            }
            response = requests.post(url, data=data)
            if response.status_code == 200:
                return response.json().get("access_token")
            return None
        
        print("="*70)
        print("PRUEBA DE INTEGRACIÓN")
        print("="*70)
        
        # Crear sistema e integración
        sistema_menu = crear_sistema_menu(DATAVERSE_URL, get_token)
        integracion = IntegracionMenuWhatsApp(sistema_menu)
        
        # Simular mensajes de usuario
        mensajes_prueba = [
            "hola",
            "1",
            "opcion 2",
            "99",
            "menu",
            "texto aleatorio"
        ]
        
        print("\n📱 SIMULANDO MENSAJES DE USUARIO:\n")
        
        for mensaje in mensajes_prueba:
            print(f"\n👤 Usuario: {mensaje}")
            respuesta = integracion.procesar_mensaje_usuario(mensaje, "573001234567")
            print(f"🤖 Bot [{respuesta['tipo']}]:")
            print(f"   {respuesta['texto'][:100]}{'...' if len(respuesta['texto']) > 100 else ''}")
        
        print("\n" + "="*70)
        print("✅ Prueba completada")
        
    except Exception as e:
        print(f"❌ Error: {e}")
