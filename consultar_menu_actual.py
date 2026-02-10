"""
Consultar el menú actual que se envía en WhatsApp
"""
import requests
import json

def consultar_menu():
    """Verificar qué menú se está enviando"""
    
    print("\n" + "="*70)
    print("CONSULTA DE MENÚ ACTUAL DE WHATSAPP")
    print("="*70)
    
    # Simular mensaje pidiendo "menu"
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
                            "name": "Usuario Test Menu"
                        },
                        "wa_id": "999999999"
                    }],
                    "messages": [{
                        "from": "999999999",
                        "id": "test_menu_" + str(int(__import__('time').time())),
                        "timestamp": str(int(__import__('time').time())),
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
    
    try:
        # Enviar petición
        response = requests.post(
            "http://localhost:5000/webhook",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"\n📥 Respuesta: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Webhook procesó correctamente")
            print("\n💡 El menú se envió al usuario por WhatsApp")
            print("   (Revisa los logs del backend para ver el contenido)")
            
            # Obtener conversaciones para ver el último mensaje enviado
            import time
            time.sleep(1)
            
            conv_response = requests.get("http://localhost:5000/api/conversations")
            if conv_response.status_code == 200:
                conversations = conv_response.json().get("conversations", [])
                
                # Buscar la conversación de nuestro usuario test
                test_conv = None
                for conv in conversations:
                    if conv.get("phone") == "999999999":
                        test_conv = conv
                        break
                
                if test_conv:
                    print(f"\n📱 Conversación encontrada:")
                    print(f"   Nombre: {test_conv.get('name')}")
                    print(f"   Teléfono: {test_conv.get('phone')}")
                    print(f"   Último mensaje:")
                    print(f"   '{test_conv.get('last_message', 'N/A')}'")
        else:
            print(f"❌ Error: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("\n❌ No se pudo conectar al backend")
        print("   Verifica que esté corriendo en http://localhost:5000")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    consultar_menu()
