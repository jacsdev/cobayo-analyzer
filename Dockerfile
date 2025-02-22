# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos necesarios al contenedor
COPY requirements.txt .
COPY .env .
COPY app/ ./app/

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto 8090 (puerto de la API)
EXPOSE 8090

# Comando para ejecutar la API con gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8090", "--timeout", "120", "app.api:app"]