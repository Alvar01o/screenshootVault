# Utilizar una imagen base de Python 3.8
FROM python:3.8

# Establecer el directorio de trabajo
WORKDIR /app
# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y libgl1-mesa-glx
# Copiar los archivos de requerimientos e instalar las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el script del servidor
COPY udp_receiver.py .
COPY utilFunctions.py .
COPY .env .
# Exponer el puerto 5005 para el servidor UDP
EXPOSE 5005/udp

# Ejecutar el script del servidor
CMD ["python", "udp_receiver.py"]