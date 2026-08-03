import os
import json
import joblib
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# 1. Config Page
st.set_page_config(page_title="SupplyTwin AI — MRO Risk Simulator", page_icon="✈️", layout="wide")

# 2. Clé API Groq
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")

if not groq_api_key:
    st.error("⚠️ Clé GROQ_API_KEY absente. Définissez-la dans vos variables d'environnement.")
    st.stop()

client = Groq(api_key=groq_api_key)

# 3. Chargement du modèle et des options dynamiques
@st.cache_resource
def load_assets():
    bundle = joblib.load('models/mro_risk_model.pkl')
    df = pd.read_csv('data/processed_mro_ml.csv')
    
    sites = sorted(df['site_id'].unique().tolist())
    suppliers = sorted(df['supplier_id'].unique().tolist())
    families = sorted(df['part_family'].unique().tolist())
    
    return bundle['model'], bundle['features'], sites, suppliers, families

try:
    model, model_features, sites_list, suppliers_list, families_list = load_assets()
except Exception as e:
    st.error(f"Erreur d'initialisation : {e}")
    st.stop()

# 4. Header
st.title("✈️ SupplyTwin AI — MRO Supply Chain Risk Simulator")
st.markdown("**Digital Twin & Agent Décisionnel IA (Royal Air Maroc MRO)**[cite: 1]")
st.divider()

# 5. UI Layout
col_input, col_results = st.columns([1, 2])

with col_input:
    st.subheader("📋 Paramètres de la Commande")
    
    site_id = st.selectbox("Site MRO Destinataire", sites_list)
    supplier_id = st.selectbox(f"Fournisseur ({len(suppliers_list)} disponibles)", suppliers_list)
    part_family = st.selectbox(f"Famille de Pièce ({len(families_list)} catégories)", families_list)
    
    ordered_qty = st.number_input("Quantité Commandée", min_value=1, max_value=1000, value=50)
    promised_lead_time = st.slider("Délai de livraison promis (jours)", min_value=1, max_value=180, value=30)
    qty_fill_rate = st.slider("Taux d'exécution historique (Fill Rate)", min_value=0.0, max_value=1.0, value=0.85, step=0.05)
    quality_incidents_count = st.number_input("Incidents Qualité Récents du Fournisseur", min_value=0, max_value=15, value=1)
    
    btn_simulate = st.button("🚀 Lancer la Simulation AI", type="primary", use_container_width=True)

# 6. Inférence & LLM Agent
if btn_simulate:
    with col_results:
        st.subheader("📊 Résultats de la Simulation")
        
        scenario = {
            'ordered_qty': ordered_qty,
            'promised_lead_time': promised_lead_time,
            'qty_fill_rate': qty_fill_rate,
            'quality_incidents_count': quality_incidents_count,
            'site_id': site_id,
            'supplier_id': supplier_id,
            'part_family': part_family
        }
        
        # Alignement des features avec get_dummies
        df_single = pd.DataFrame([scenario])
        df_encoded = pd.get_dummies(df_single)
        df_aligned = df_encoded.reindex(columns=model_features, fill_value=0)
        
        # Calcul probabilité ML
        risk_proba = model.predict_proba(df_aligned)[0][1]
        risk_pct = risk_proba * 100
        
        # Affichage des métriques
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Risque de Retard Détecté (ML)", f"{risk_pct:.1f}%")
        with c2:
            if risk_pct >= 60:
                st.error("🔴 Risque Critique (Procédure AOG)")
            elif risk_pct >= 30:
                st.warning("🟡 Risque Modéré")
            else:
                st.success("🟢 Risque Faible")
                
        st.divider()
        
        # Génération LLM
        with st.spinner("🤖 Génération de la recommandation stratégique..."):
            system_prompt = """
            Tu es un Expert Senior en Logistique Aéronautique pour Royal Air Maroc MRO[cite: 1].
            Analyse les entrées du scénario et les résultats du modèle ML pour fournir :
            1. Diagnostic Technique (Analyse de la combinatoire Fournisseur, Famille de pièce et Incidents).
            2. Impact Site MRO (Différence d'impact selon si la livraison est vers CMN_HUB ou un site régional RAK/TNG).
            3. Directives Opérationnelles :
               - Si Incidents Qualité > 0 : protocole de sur-contrôle à la réception.
               - Si Risque > 50% : plan de transfert inter-sites (CMN/RAK/TNG) ou sourcing alternatif urgent.
            Sois synthétique, structuré et professionnel.
            """

            user_prompt = f"Données du scénario :\n{json.dumps(scenario, indent=2)}\n\nRisque ML de retard : {risk_pct:.1f}%"

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