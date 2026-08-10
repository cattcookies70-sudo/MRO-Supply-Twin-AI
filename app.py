import os
import json
import joblib
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import streamlit.components.v1 as components
from dotenv import load_dotenv
from groq import Groq

# ==========================================
# 1. CONFIGURATION DE LA PAGE
# ==========================================
st.set_page_config(page_title="SupplyTwin AI — MRO 4.0 Hub", page_icon="✈️", layout="wide")

# ==========================================
# 2. DESIGN & ANIMATIONS CSS (Royal Air Maroc Cockpit)
# ==========================================
def inject_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* --- ANIMATIONS D'ARRIÈRE-PLAN --- */
    
    /* Animation 1 : Trajectoire d'avion en arrière-plan (Opacité 6%) */
    @keyframes planeDrift {
        0% {
            transform: translate(-150px, 85vh) scale(0.7) rotate(-22deg);
            opacity: 0;
        }
        10% { opacity: 0.06; }
        90% { opacity: 0.06; }
        100% {
            transform: translate(105vw, -150px) scale(0.7) rotate(-22deg);
            opacity: 0;
        }
    }

    /* Animation 2 : Pulsation de la grille radar */
    @keyframes radarPulse {
        0%, 100% { opacity: 0.02; }
        50% { opacity: 0.05; }
    }

    /* Avion en arrière-plan */
    .stApp::after {
        content: "" !important;
        position: fixed !important;
        top: 0; left: 0;
        width: 140px; height: 140px;
        background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23C8102E"><path d="M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z"/></svg>') !important;
        background-size: contain !important;
        background-repeat: no-repeat !important;
        pointer-events: none !important;
        z-index: 0 !important;
        animation: planeDrift 30s linear infinite !important;
    }

    /* Grille tactique radar */
    .stApp::before {
        content: "" !important;
        position: fixed !important;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: 
            linear-gradient(rgba(200, 16, 46, 0.2) 1px, transparent 1px),
            linear-gradient(90deg, rgba(200, 16, 46, 0.2) 1px, transparent 1px) !important;
        background-size: 70px 70px !important;
        pointer-events: none !important;
        z-index: 0 !important;
        animation: radarPulse 6s ease-in-out infinite !important;
    }

    /* --- STYLES D'INTERFACE --- */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0B0F19 0%, #111827 50%, #0B0F19 100%) !important;
        background-attachment: fixed !important;
        color: #E5E7EB !important;
    }
    
    .main .block-container {
        background: transparent !important;
        padding: 2rem 3rem 4rem 3rem !important;
        max-width: 1400px !important;
        position: relative !important;
        z-index: 1 !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: #111827; }
    ::-webkit-scrollbar-thumb { background: #374151; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #C8102E; }

    /* Typographie */
    h1 {
        font-weight: 800 !important;
        font-size: 2.4rem !important;
        letter-spacing: -0.02em !important;
        color: #F9FAFB !important;
        text-shadow: 0 2px 10px rgba(200, 16, 46, 0.2) !important;
        margin-bottom: 0.5rem !important;
    }
    
    h2, h3 {
        font-weight: 700 !important;
        color: #F3F4F6 !important;
        letter-spacing: -0.01em !important;
        margin-top: 1.5rem !important;
    }
    
    h4, h5, h6, .stMarkdown p {
        color: #D1D5DB !important;
        font-weight: 400 !important;
        line-height: 1.6 !important;
    }
    
    .stCaption {
        color: #9CA3AF !important;
        font-size: 0.85rem !important;
        letter-spacing: 0.02em !important;
        text-transform: uppercase !important;
        font-weight: 500 !important;
    }

    /* Onglets Cockpit */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(31, 41, 55, 0.6) !important;
        backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(55, 65, 81, 0.5) !important;
        border-radius: 16px !important;
        padding: 6px !important;
        gap: 6px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3) !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: #9CA3AF !important;
        border-radius: 12px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        border: none !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(200, 16, 46, 0.1) !important;
        color: #F9FAFB !important;
        transform: translateY(-1px) !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #C8102E 0%, #9B1B30 100%) !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 15px rgba(200, 16, 46, 0.35) !important;
        font-weight: 700 !important;
    }
    
    .stTabs [data-baseweb="tab-highlight"] { background: transparent !important; }

    /* Boutons RAM */
    .stButton > button {
        background: linear-gradient(135deg, #C8102E 0%, #9B1B30 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.02em !important;
        text-transform: uppercase !important;
        box-shadow: 0 4px 15px rgba(200, 16, 46, 0.25) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(200, 16, 46, 0.4) !important;
        background: linear-gradient(135deg, #D4203A 0%, #C8102E 100%) !important;
    }

    /* Cartes Métriques */
    [data-testid="stMetric"] {
        background: rgba(31, 41, 55, 0.7) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(55, 65, 81, 0.6) !important;
        border-radius: 16px !important;
        padding: 1.25rem !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        color: #9CA3AF !important;
        text-transform: uppercase !important;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        color: #F9FAFB !important;
    }

    /* Formulaires & Inputs */
    .stSelectbox > div > div, .stNumberInput > div > div {
        background: rgba(31, 41, 55, 0.8) !important;
        border: 1px solid #374151 !important;
        border-radius: 12px !important;
        color: #F3F4F6 !important;
    }

    /* Alertes */
    .stAlert {
        border-radius: 14px !important;
        backdrop-filter: blur(8px) !important;
    }

    /* Séparateur */
    hr {
        border: 0 !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent 0%, #374151 20%, #C8102E 50%, #374151 80%, transparent 100%) !important;
    }

    /* Multi-média & Graphiques */
    .stPlotlyChart, iframe {
        border-radius: 16px !important;
        border: 1px solid rgba(55, 65, 81, 0.5) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Application immédiate du style
inject_custom_css()

# ==========================================
# 3. INITIALISATION GROQ API (AVEC TOLÉRANCE RÉSEAU)
# ==========================================
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")

if not groq_api_key:
    st.error("⚠️ Clé GROQ_API_KEY absente. Définissez-la dans vos variables d'environnement.")
    st.stop()

# Configuration robuste avec retries et timeout
client = Groq(
    api_key=groq_api_key,
    timeout=20.0,
    max_retries=3
)

# ==========================================
# 4. CHARGEMENT DES MODÈLES ET MÉTADONNÉES
# ==========================================
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

# ==========================================
# 5. EN-TÊTE PRINCIPAL
# ==========================================
st.title("✈️ SupplyTwin AI — MRO Industry 4.0 Suite")
st.markdown("**Plateforme Intégrée de Supervision MRO & Maintenance Prédictive (Royal Air Maroc)**")

# ==========================================
# 6. ONGLETS DE NAVIGATION
# ==========================================
tab_sim, tab_map, tab_3d = st.tabs([
    "🚀 Simulateur de Risque & Agent IA", 
    "🗺️ Jumeau Numérique 2D (Entrepôt CMN)", 
    "📦 Inspection 3D & Major Components"
])

# ==========================================
# TAB 1 : SIMULATEUR DE RISQUE ML + LLM
# ==========================================
with tab_sim:
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
            
            df_single = pd.DataFrame([scenario])
            df_encoded = pd.get_dummies(df_single)
            df_aligned = df_encoded.reindex(columns=model_features, fill_value=0)
            
            risk_proba = model.predict_proba(df_aligned)[0][1]
            risk_pct = risk_proba * 100
            
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
            
            with st.spinner("🤖 Génération de la recommandation stratégique..."):
                system_prompt = """
                Tu es un Expert Senior en Logistique Aéronautique pour Royal Air Maroc MRO.
                Analyse les entrées du scénario et les résultats du modèle ML pour fournir :
                1. Diagnostic Technique (Fournisseur, Famille de pièce et Incidents).
                2. Impact Site MRO (Livraison vers CMN_HUB vs sites régionaux RAK/TNG).
                3. Directives Opérationnelles (Sur-contrôle qualité, transferts inter-sites).
                """

                user_prompt = f"Données du scénario :\n{json.dumps(scenario, indent=2)}\n\nRisque ML de retard : {risk_pct:.1f}%"

                try:
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

                except Exception as e:
                    st.warning("⚠️ **Instabilité réseau détectée :** Impossible de joindre l'agent IA pour le moment.")
                    st.info("💡 **Conseil :** La connexion Internet a subi une micro-coupure. Cliquez à nouveau sur 'Lancer la Simulation AI'.")

# ==========================================
# TAB 2 : JUMEAU NUMÉRIQUE 2D
# ==========================================
with tab_map:
    st.subheader("🗺️ Cartographie Spatiale de l'Entrepôt MRO (Casablanca CMN Hub)")
    st.caption("Visualisation en temps réel de l'état des zones de stockage et du niveau de risque par famille de pièces.")

    zones_data = [
        {"Zone": "Rack A1 - Avionics", "X": 1, "Y": 3, "Stock": "8,200 pcs", "Risk": "Modéré (32%)", "Status": "#f39c12"},
        {"Zone": "Rack A2 - Engines Parts", "X": 3, "Y": 3, "Stock": "1,450 pcs", "Risk": "Critique (78%)", "Status": "#C8102E"},
        {"Zone": "Rack B1 - Landing Gear", "X": 5, "Y": 3, "Stock": "3,100 pcs", "Risk": "Faible (12%)", "Status": "#10B981"},
        {"Zone": "Rack B2 - Hydraulics", "X": 1, "Y": 1, "Stock": "5,600 pcs", "Risk": "Modéré (45%)", "Status": "#f39c12"},
        {"Zone": "Rack C1 - Structure", "X": 3, "Y": 1, "Stock": "12,000 pcs", "Risk": "Faible (8%)", "Status": "#10B981"},
        {"Zone": "Rack C2 - Cabin & Fasteners", "X": 5, "Y": 1, "Stock": "25,400 pcs", "Risk": "Critique (65%)", "Status": "#C8102E"}
    ]
    
    df_zones = pd.DataFrame(zones_data)

    fig = go.Figure()

    for _, row in df_zones.iterrows():
        fig.add_trace(go.Scatter(
            x=[row["X"]],
            y=[row["Y"]],
            mode="markers+text",
            marker=dict(size=60, color=row["Status"], symbol="square", line=dict(width=2, color="white")),
            text=row["Zone"].split(" - ")[1],
            textposition="middle center",
            textfont=dict(color="white", size=11, family="Arial Black"),
            hoverinfo="text",
            hovertext=f"<b>{row['Zone']}</b><br>Stock Dispo : {row['Stock']}<br>Risque MRO : {row['Risk']}"
        ))

    fig.update_layout(
        title="Plan de Masse du Hangar de Stockage MRO",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 6]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 4]),
        height=450,
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig, use_container_width=True)

    k1, k2, k3 = st.columns(3)
    k1.metric("Zones Sous Contrôle (Vert)", "2 Zones", "Stock Optimal")
    k2.metric("Zones Sous Vigilance (Orange)", "2 Zones", "Attention Lead-Time")
    k3.metric("Zones sous Alerte AOG (Rouge)", "2 Zones", "Action Recommandée")

# ==========================================
# TAB 3 : INSPECTION 3D & MAJOR COMPONENTS
# ==========================================
with tab_3d:
    st.subheader("📦 Inspection 3D & Cartographie des Composants Aéronautiques")
    st.caption("Inspectez l'appareil en 3D interactive pour localiser l'ensemble des sous-systèmes MRO (Boeing 787 Major Components).")

    mro_3d_catalog = {
        "Boeing 787 Dreamliner (Composants Majeurs)": {
            "type": "sketchfab",
            "embed_id": "7b850cd2e3eb4231b5e8d670eb58de90",
            "family": "Structure / Multi-Systèmes MRO",
            "part_id": "B787_DREAMLINER_FULL",
            "stock_status": "🟢 Inspection C-Check & Cartographie",
            "safety_note": "Explorez les points d'annotation (1 à 24) pour inspecter l'ensemble des composants aéronautiques."
        },
        "Train d'Atterrissage Boeing 787 (Landing Gear)": {
            "type": "sketchfab",
            "embed_id": "47fc0c93058e459183177d549c836081",
            "family": "Landing Gear",
            "part_id": "PART_LDG_787",
            "stock_status": "🟢 Stock Disponible (2 unités)",
            "safety_note": "Contrôle d'usure des vérins hydrauliques à effectuer avant assemblage."
        },
        "Sous-Ensemble Moteur (Engine Component)": {
            "type": "model_viewer",
            "url": "https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/2CylinderEngine/glTF-Binary/2CylinderEngine.glb",
            "family": "Engines Parts",
            "part_id": "PART_ENG_088",
            "stock_status": "🟡 Sous Vigilance",
            "safety_note": "Inspection du jeu d'engrenage en atelier MRO."
        }
    }

    col_select, col_info = st.columns([1, 1])

    with col_select:
        selected_part = st.selectbox("🔍 Choisir le composant à inspecter :", list(mro_3d_catalog.keys()))
        part_data = mro_3d_catalog[selected_part]

    with col_info:
        st.markdown(f"**ID Pièce :** `{part_data['part_id']}` | **Famille :** `{part_data['family']}`")
        st.markdown(f"**État du Stock :** {part_data['stock_status']}")
        st.caption(f"⚠️ *Directive Maintenance :* {part_data['safety_note']}")

    st.divider()

    if part_data["type"] == "sketchfab":
        sketchfab_url = f"https://sketchfab.com/models/{part_data['embed_id']}/embed?autostart=1&internal=1&ui_infos=0&ui_snapshots=0&ui_stop=0&ui_watermark=0"
        components.iframe(sketchfab_url, height=520, scrolling=False)
    else:
        model_viewer_code = f"""
        <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.4.0/model-viewer.min.js"></script>
        <div style="display: flex; justify-content: center; align-items: center; background-color: #0B0F19; padding: 15px; border-radius: 16px; border: 1px solid rgba(55, 65, 81, 0.5);">
            <model-viewer 
                src="{part_data['url']}" 
                alt="{selected_part}" 
                auto-rotate 
                camera-controls 
                ar 
                shadow-intensity="1" 
                style="width: 100%; height: 480px; background-color: #0B0F19;">
            </model-viewer>
        </div>
        """
        components.html(model_viewer_code, height=540)

    st.info("💡 **Astuce Démo :** Utilisez la souris pour pivoter/zoomer autour du Boeing 787 et cliquez sur les puces numérotées pour passer d'un composant à l'autre !")