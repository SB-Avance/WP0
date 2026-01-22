# Configuración global y clave secreta para JWT
import os

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
