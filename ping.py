import os
import time

# Lista de direcciones IP a monitorear
direcciones_ip = [
    "8.8.8.8",     # Google DNS
    "1.1.1.1",     # Cloudflare DNS
#    "192.168.0.1", # IP local típica de routers
#    "206.190.36.45", # Yahoo
    "142.250.187.36", # Google
#    "8.26.56.26",     # Comodo Secure DNS
#    "64.233.160.0",   # Otra IP de Google
#    "208.67.222.222", # OpenDNS
#    "185.228.168.9",  # CleanBrowsing DNS
#    "198.41.0.4"      # DNS raíz
]

# Registro de resultados
registro_caidas = {ip: False for ip in direcciones_ip}  # Estado inicial de todas las IPs

def hacer_ping(direccion):
    """
    Realiza un ping a una dirección IP y devuelve True si el ping tuvo éxito.
    """
    respuesta = os.system(f"ping -c 1 -w 1 {direccion} > /dev/null 2>&1")
    return respuesta == 0

def monitorear_ips():
    """
    Monitorea las direcciones IP cada 10 segundos y registra/alerta caídas.
    """
    while True:
        print("\n--- Verificando conexión de direcciones IP ---")
        for ip in direcciones_ip:
            esta_activa = hacer_ping(ip)
            if esta_activa:
                print(f"[OK] {ip} está activa.")
                # Si la IP acaba de recuperarse, notificar
                if registro_caidas[ip]: # Estaba caída previamente
                    print(f"[RECUPERADA] {ip} está de vuelta en línea.")
                    registro_caidas[ip] = False
            else:
                print(f"[ALERTA] {ip} está caída.")
                # Si la IP no estaba en estado de caída previamente, registrar
                if not registro_caidas[ip]:
                    print(f"[NUEVO ERROR] ¡CAÍDA detectada! {ip}")
                    registro_caidas[ip] = True
        time.sleep(10)  # Esperar 10 segundos antes de la siguiente comprobación

# Ejecutar el script de monitoreo.
if __name__ == "__main__":
    monitorear_ips()