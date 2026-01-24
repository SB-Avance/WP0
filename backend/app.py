"""
Archivo de entrada para Azure App Service
Importa la aplicación Flask desde back.py
"""
from back import app

if __name__ == "__main__":
    app.run()
