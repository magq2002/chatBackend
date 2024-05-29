# Usa una imagen base de Python
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Instala las dependencias de Python
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN python -m nltk.downloader punkt wordnet stopwords

# Copia el resto de los archivos del proyecto
COPY . .

# Establece un valor predeterminado para la variable PORT si no está definida
ARG PORT=8000
ENV PORT=${PORT}

# Expone el puerto en el que correrá la aplicación
EXPOSE ${PORT}

# Inicia la aplicación
CMD ["sh", "-c", "gunicorn wsgi:app --bind 0.0.0.0:${PORT}"]
