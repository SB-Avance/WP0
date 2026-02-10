"""
Simular mensaje de WhatsApp real y ver la respuesta
"""
import requests
import json
import time

def test_whatsapp_menu():
    """Simular mensaje de WhatsApp pidiendo menu"""
    
    # Simular webhook de WhatsApp real
    payload = {
        "object": "whatsapp_business_account",
        "entry": [{
            "id": "PROD_TEST",
            "changes": [{
                "value": {
                    "messaging_product": "whatsapp",
                    "metadata": {
                        "display_phone_number": "12345678",
                        "phone_number_id": "510287455510831"
                    },
                    "contacts": [{
                        "profile": {
                            "name": "Usuario Real"
                        },
                        "wa_id": "573001234567"
                    }],
                    "messages": [{
                        "from": "573001234567",
                        "id": f"wamid_{int(time.time())}",
                        "timestamp": str(int(time.time())),
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
    print("PRUEBA: MENSAJE 'menu' DESDE WHATSAPP")
    print("="*70)
    print("\nEnviando webhook al backend...")
    
    try:
        response = requests.post(
            "http://localhost:5000/webhook",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"\n✅ Respuesta HTTP: {response.status_code}")
        
        if response.status_code == 200:
            print("\n✅ Webhook procesado correctamente")
            print("\n📱 El menu se envio al usuario por WhatsApp")
            print("\n💡 Revisa los LOGS DEL BACKEND para ver el contenido del menu:")
            print("   Busca las lineas que empiezan con [MENU_TEXT]")
            
            # Esperar un momento para ver los logs
            time.sleep(1)
            
            # Intentar ver las conversaciones para confirmar
            print("\n📊 Verificando base de datos...")
            conv_response = requests.get("http://localhost:5000/api/conversations", timeout=5)
            
            if conv_response.status_code == 200:
                data = conv_response.json()
                convs = data.get("conversations", [])
                
                # Buscar nuestra conversacion de prueba
                test_conv = None
                for conv in convs:
                    if conv.get("phone") == "573001234567":
                        test_conv = conv
                        break
                
                if test_conv:
                    print(f"\n✅ Conversacion encontrada en BD:")
                    print(f"   Telefono: {test_conv.get('phone')}")
                    print(f"   Nombre: {test_conv.get('name')}")
                    print(f"   Grupo: {test_conv.get('group')}")
                    
                    # Obtener mensajes
                    msg_response = requests.get(
                        f"http://localhost:5000/api/messages/{test_conv.get('phone')}",
                        timeout=5
                    )
                    
                    if msg_response.status_code == 200:
                        messages = msg_response.json().get("messages", [])
                        
                        # Buscar el mensaje de respuesta del bot
                        bot_messages = [m for m in messages if m.get("direction") == "outgoing"]
                        
                        if bot_messages:
                            last_bot_msg = bot_messages[-1]
                            print(f"\n📤 ULTIMO MENSAJE ENVIADO POR EL BOT:")
                            print("="*70)
                            print(last_bot_msg.get("body", ""))
                            print("="*70)
                        else:
                            print("\n⚠️  No se encontraron mensajes salientes del bot en BD")
            else:
                print(f"\n⚠️  No se pudo verificar BD: HTTP {conv_response.status_code}")
        else:
            print(f"\n❌ Error HTTP {response.status_code}")
            print(f"   Respuesta: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: No se pudo conectar al backend")
        print("   Verifica que este corriendo en http://localhost:5000")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    test_whatsapp_menu()
