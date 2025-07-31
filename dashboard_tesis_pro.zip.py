import requests

url = "https://8000-i1phkgubcw5gabur8xq3a-8a410218.manusvm.computer/dashboard_tesis_pro.zip"

filepath = "./dashboard_tesis_pro.zip"

try:
    response = requests.get(url, stream=True )
    response.raise_for_status()  # Lanza una excepción para códigos de estado de error (4xx o 5xx)
    with open(filepath, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Archivo descargado exitosamente a: {filepath}")
except requests.exceptions.ConnectionError as e:
    print(f"Error de conexión: Asegúrate de que el servidor HTTP en el sandbox esté corriendo y sea accesible. {e}")
except requests.exceptions.RequestException as e:
    print(f"Error al descargar el archivo: {e}")

