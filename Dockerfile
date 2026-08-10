# 1. Image de base Python optimisée
FROM python:3.10-slim

# 2. Répertoire de travail dans le conteneur
WORKDIR /app

# 3. Installation des dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# 4. Copie des fichiers de configuration et installation des packages Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copie de l'ensemble du code source, modèles et données
COPY . .

# 6. Exposer le port par défaut de Streamlit
EXPOSE 8501

# 7. Configuration de santé pour Streamlit
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# 8. Commande de lancement de l'application
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]