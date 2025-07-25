# On part d'une image Python légère et officielle
FROM python:3.10-slim

# On installe FFmpeg, l'outil ultime pour l'audio/vidéo
RUN apt-get update && apt-get install -y ffmpeg

# On installe Flask, un micro-framework web très simple
RUN pip install Flask

# On définit le dossier de travail à l'intérieur du conteneur
WORKDIR /app

# On copie le code de notre application
COPY app.py .

# On expose le port sur lequel notre service va écouter
EXPOSE 5000

# La commande pour démarrer notre service
CMD ["python", "app.py"]
