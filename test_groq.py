import os
from dotenv import find_dotenv, load_dotenv
from groq import Groq

# Force le chargement du fichier .env par-dessus les variables système
load_dotenv(find_dotenv(), override=True)

key = os.getenv("GROQ_API_KEY")

print(f"Clé chargée : {key}")

client = Groq(api_key=key)

res = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "Test de connexion. Réponds juste OK."}],
)

print("Réponse Groq :", res.choices[0].message.content)