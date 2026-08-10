# 1. Image de base Python optimisée
FROM python:3.10-slim

# 2. Répertoire de travail dans le conteneur
WORKDIR /app

# 3. Copie et installation des dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copie de l'ensemble du code source, modèles et fichiers
COPY . .

# 5. Exposer le port Streamlit
EXPOSE 8501

# 6. Commande de lancement de l'application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]