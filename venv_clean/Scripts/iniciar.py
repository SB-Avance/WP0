import subprocess
import time

def iniciar_whatsapp_manager():
    print("Iniciando WhatsApp Manager desde Python...")

    # 1. Iniciar el Backend en una nueva ventana de CMD
    # El comando 'start' abre la ventana, 'cmd /k' la mantiene abierta tras ejecutar
    subprocess.Popen(
        'start cmd /k "cd C:\\VS\\CLAUDE-1\\backend && python back.py"', 
        shell=True
    )

    # 2. Tiempo de espera (Equivalente al timeout /t 2)
    time.sleep(2)

    # 3. Iniciar la App Móvil (Flet/Python) en otra ventana
    subprocess.Popen(
        'start cmd /k "cd C:\\VS\\CLAUDE-1\\mobile && python main.py"', 
        shell=True
    )

    print("Procesos lanzados con éxito.")

if __name__ == "__main__":
    iniciar_whatsapp_manager()