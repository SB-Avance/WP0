import requests
import os

BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")

# Test de registro y login

def test_register_and_login():
    print("Test: Registro y Login")
    # Registro (solo admin puede crear, así que simula un admin ya creado)
    # Primero login admin
    admin_login = requests.post(f"{BASE_URL}/api/login", json={"correo": "admin@erp.com", "clave": "admin123"})
    if admin_login.status_code != 200:
        print("[ERROR] Login admin falló:", admin_login.text)
        return
    token = admin_login.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    # Crear usuario
    user_data = {"nombre": "Test User", "correo": "test@erp.com", "clave": "test123", "rol": "usuario"}
    r = requests.post(f"{BASE_URL}/api/users", json=user_data, headers=headers)
    print("Crear usuario:", r.status_code, r.text)
    # Login usuario
    login = requests.post(f"{BASE_URL}/api/login", json={"correo": "test@erp.com", "clave": "test123"})
    print("Login usuario:", login.status_code, login.text)

def test_list_users():
    print("Test: Listar usuarios (admin)")
    admin_login = requests.post(f"{BASE_URL}/api/login", json={"correo": "admin@erp.com", "clave": "admin123"})
    if admin_login.status_code != 200:
        print("[ERROR] Login admin falló:", admin_login.text)
        return
    token = admin_login.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{BASE_URL}/api/users", headers=headers)
    print("Listar usuarios:", r.status_code, r.text)

def test_conversations_and_messages():
    print("Test: Conversaciones y Mensajes")
    login = requests.post(f"{BASE_URL}/api/login", json={"correo": "test@erp.com", "clave": "test123"})
    if login.status_code != 200:
        print("[ERROR] Login usuario falló:", login.text)
        return
    token = login.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{BASE_URL}/api/conversations", headers=headers)
    print("Conversaciones:", r.status_code, r.text)
    # Si hay conversaciones, prueba mensajes
    if r.status_code == 200 and r.json().get("conversations"):
        phone = r.json()["conversations"][0]["phone"]
        m = requests.get(f"{BASE_URL}/api/messages/{phone}", headers=headers)
        print("Mensajes:", m.status_code, m.text)

def run_all():
    test_register_and_login()
    test_list_users()
    test_conversations_and_messages()

if __name__ == "__main__":
    run_all()
