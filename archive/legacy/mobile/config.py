"""
Configuración de URLs para la aplicación móvil
"""

import os

# Determinar el entorno
ENVIRONMENT = os.getenv("ENVIRONMENT", "LOCAL")  # LOCAL, AZURE, PRODUCTION

# URLs por entorno
URLS = {
    "LOCAL": "http://localhost:5000",
    "AZURE": "https://whatsapp-flask-app-f4gsb7dhhybcg6f6.eastus-01.azurewebsites.net",
    "PRODUCTION": os.getenv("PRODUCTION_URL", "http://localhost:5000"),
}

# URL base activa
API_BASE_URL = URLS.get(ENVIRONMENT, URLS["LOCAL"])

print(f"🌐 [CONFIG] Entorno: {ENVIRONMENT}")
print(f"🌐 [CONFIG] API Base URL: {API_BASE_URL}")
