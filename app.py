import os
import joblib
import pandas as pd
import json
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# 1. Configuration de la page Streamlit
st.set_page_config(
    page_title="SupplyTwin AI — MRO Risk Simulator",
    page_icon="✈️",
    layout="wide"
)

# 2. Chargement de l'environnement et des clés API
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")

if not groq_api_key:
    st.error("⚠️ Clé GROQ_API_KEY non trouvée. Vérifie ton fichier .env ou tes secrets Streamlit.")
    st.stop()

client = Groq(api_key=groq_api_key)

# 3. Chargement du modèle ML
@st.cache_resource
def load_ml_model():
    model_data = joblib.load('models/mro_risk_model.pkl')
    return model_data['model'], model_data['features']

try:
    model, features = load_ml_model()
except Exception as e:
    st.error(f"Erreur lors du chargement du modèle ML : {e}")
    st.stop()

# 4. En-tête de l'application
st.title("✈️ SupplyTwin AI — MRO Supply Chain Risk Simulator")
st.markdown("""
**Assistant IA & Jumeau Numérique MRO (Royal Air Maroc)**  
Simulez le risque de retard/rupture d'une commande de pièces aéronautiques et obtenez un plan d'action d'urgence.
""")

st.divider()

# 5. Interface Utilisateur (Sidebar & Formulaire)
col_input, col_results = st.columns([1, 2])

with col_input:
    st.subheader("📋 Paramètres de la Commande")
    
    site_id = st.selectbox("Site MRO", ["CMN_HUB", "RAK_SITE", "TNG_SITE"], index=0)
    supplier_id = st.selectbox("Fournisseur", ["SUPP_01_AVIONICS", "SUPP_02_ENGINES", "SUPP_03_CABIN"], index=0)
    ordered_qty = st.number_input("Quantité Commandée", min_value=1, max_value=1000, value=50)
    promised_lead_time = st.slider("Délai de livraison promis (jours)", min_value=1, max_value=180, value=90)
    qty_fill_rate = st.slider("Taux de livraison historique (Fill Rate)", min_value=0.0, max_value=1.0, value=0.70, step=0.05)
    
    btn_simulate = st.button("🚀 Lancer la Simulation AI", type="primary", use_container_width=True)

# 6. Moteur de simulation (ML + LLM)
if btn_simulate:
    with col_results:
        st.subheader("📊 Résultats de la Simulation")
        
        # Structuration de la donnée pour le ML
        scenario = {
            'ordered_qty': ordered_qty,
            'promised_lead_time': promised_lead_time,
            'qty_fill_rate': qty_fill_rate,
            'site_id': site_id,
            'supplier_id': supplier_id
        }
        
        # Alignment des variables avec le One-Hot Encoding du modèle
        df_single = pd.DataFrame([scenario])
        df_encoded = pd.get_dummies(df_single)
        df_aligned = df_encoded.reindex(columns=features, fill_value=0)
        
        # Prédiction ML
        risk_proba = model.predict_proba(df_aligned)[0][1]
        risk_pct = risk_proba * 100
        
        # Affichage du score avec indicateur visuel
        col_metric1, col_metric2 = st.columns(2)
        with col_metric1:
            st.metric(label="Risque de Retard Détecté (ML)", value=f"{risk_pct:.1f}%")
        with col_metric2:
            if risk_pct >= 60:
                st.error("🔴 Risque Élevé (Alerte AOG)")
            elif risk_pct >= 30:
                st.warning("🟡 Risque Modéré")
            else:
                st.success("🟢 Risque Faible")
                
        st.divider()
        
        # Génération de la réponse LLM Groq
        with st.spinner("🤖 Génération du plan d'action MRO par l'Agent IA (Groq)..."):
            system_prompt = """
            Tu es un Expert Senior en Supply Chain Aéronautique et MRO pour la compagnie Royal Air Maroc.
            Analyse le score de risque produit par le modèle ML et fournis une recommandation métier basée sur nos protocoles MRO :
            1. **Diagnostic du Risque** (Analyse des facteurs Lead Time, Fill Rate, Fournisseur)
            2. **Impact Flotte & Risque AOG** (Avion au sol)
            3. **Plan d'Action Logistique Urgent** :
               - Contrôle du stock disponible (Safety Stock / On-Hand)
               - Protocole AOG Desk si risque > 60%
               - Réallocation inter-sites (CMN / RAK / TNG)
            """

            user_prompt = f"""
            Alerte Commande Pièce Aéronautique :
            - Paramètres : {json.dumps(scenario, indent=2)}
            - Probabilité de Retard Calculée par ML : {risk_pct:.1f}%

            Fournis ton analyse décisionnelle.
            """

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2
            )
            
            st.markdown("### 📝 Recommandation Stratégique MRO")
            st.markdown(response.choices[0].message.content)