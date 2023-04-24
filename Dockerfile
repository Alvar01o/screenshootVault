# Utiliza la imagen base de Python 3.8
FROM python:3.8

# Configura las variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instala las dependencias del sistema operativo
RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat \
    && rm -rf /var/lib/apt/lists/*

# Crea y configura el directorio de trabajo
RUN mkdir /app
WORKDIR /app

# Instala las dependencias de Python
COPY requirements.txt /app/
RUN pip install -r requirements.txt