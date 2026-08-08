# ✈️ SupplyTwin AI — MRO Supply Chain Risk Simulator

 Un jumeau numérique et agent décisionnel IA développé pour optimiser la chaîne logistique MRO (Maintenance, Repair, and Overhaul) de **Royal Air Maroc**.

## 📌 Aperçu du Projet
Ce projet combine le **Machine Learning** et les **LLMs** pour prédire les risques de retard/rupture de pièces aéronautiques critiques et générer des plans d'action logistiques en temps réel.

### ⚙️ Architecture & Pipeline
1. **Data Pipeline** : Jointures multi-tables (`purchase_orders`, `parts_master`, `quality_incidents`) avec gestion dynamique de 40 fournisseurs, 7 familles de pièces et des historiques d'incidents.
2. **Predictive Model (ML)** : Algorithme `GradientBoostingClassifier` prédisant la probabilité de retard de livraison (ROC-AUC ~0.85+).
3. **Decision Agent (LLM)** : Agent IA (Llama 3.3 via Groq) analysant les scores de risque et préconisant des actions d'urgence (procédures AOG, transferts inter-sites CMN/RAK/TNG, sur-contrôles qualité).
4. **UI Dashboard** : Application interactive développée sous **Streamlit**.

---

## 🛠️ Installation & Exécution

```bash
# 1. Cloner le projet
git clone [https://github.com/ton-username/mro-supply-twin-ai.git](https://github.com/cattcookies70-sudo/MRO-Supply-Twin-AI.git)
cd mro-supply-twin-ai

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer la préparation des données et l'entraînement ML
python notebooks/01_data_prep.py
python notebooks/02_train_model.py

# 4. Lancer l'application Web
streamlit run app.py