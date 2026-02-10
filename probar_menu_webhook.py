"""
Probar carga de menú desde webhook
"""
import requests
import json

def probar_menu_webhook():
    """Simular petición de webhook para verificar menú"""
    
    # Simular mensaje de WhatsApp solicitando menú
    payload = {
        "object": "whatsapp_business_account",
        "entry": [{
            "id": "TEST",
            "changes": [{
                "value": {
                    "messaging_product": "whatsapp",
                    "metadata": {
                        "display_phone_number": "12345",
                        "phone_number_id": "510287455510831"
                    },
                    "contacts": [{
                        "profile": {
                            "name": "Usuario Test"
                        },
                        "wa_id": "123456789"
                    }],
                    "messages": [{
                        "from": "123456789",
                        "id": "test_msg_id",
                        "timestamp": "1234567890",
                        "text": {
                            "body": "menu"
                        },
                        "type": "text"
                    }]
                },
                "field": "messages"
            }]
        }]
    }
    
    print("\n" + "="*70)
    print("PRUEBA DE MENÚ DESDE WEBHOOK")
    print("="*70)
    
    print("\n📤 Enviando petición al webhook...")
    
    try:
        response = requests.post(
            "http://localhost:5000/webhook",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"\n📥 Respuesta HTTP: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Webhook procesó correctamente la petición")
            
            # Esperar un momento y ver logs del backend
            print("\n💡 Revisa la consola del backend para ver:")
            print("   - [WEBHOOK] Menú cargado desde chatbot 'XXX': N opciones")
            print("   - Listado de cada opción [1] Nombre (tipo: xxx)")
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            
    except Exception as e:
        print(f"\n❌ Error al contactar webhook: {e}")
        print("\n⚠️  Verifica que el backend esté corriendo:")
        print("   python backend/back.py")

if __name__ == "__main__":
    probar_menu_webhook()
