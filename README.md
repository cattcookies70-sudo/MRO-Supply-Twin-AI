# ✈️ MRO Supply Twin AI — Industry 4.0 Suite

![Python](https://img.shields.io/badge/Python-3.10-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![AWS Ready](https://img.shields.io/badge/AWS-EC2%20Ready-orange)
![Llama-3](https://img.shields.io/badge/Groq-Llama--3.3--70B-green)

An End-to-End AI-driven Digital Twin designed for **Maintenance, Repair, and Overhaul (MRO)** aeronautical supply chains (Royal Air Maroc - Casablanca CMN Hub). 

This multi-tab application combines **Machine Learning**, **LLM Decision Support (LLaMA-3 via Groq)**, **2D Warehouse Spatial Mapping**, and **3D Interactive Component Inspection**.

---

## 📸 Cockpit Overview & Modules

### 🚀 Tab 1: AI Risk Simulator & Decision Agent
Predicts component stockout and delivery delay risks using Machine Learning (`Scikit-Learn`), combined with an LLM Agent providing structured, real-time operational recommendations for MRO managers.

![Tab 1 - AI Simulator](./assets/dashboard.png)

---

### 🗺️ Tab 2: 2D Digital Twin (Casablanca CMN Warehouse)
Provides real-time spatial mapping of warehouse storage racks and part families, highlighting risk levels (Optimal, Warning, Critical AOG) across storage zones.

![Tab 2 - 2D Digital Twin](./assets/2D.png)

---

### 📦 Tab 3: 3D Interactive Component Inspection
Interactive 3D visualization of major aeronautical structures (Boeing 787 components, landing gears, engines) allowing MRO engineers to inspect sub-assemblies and verify stock availability before maintenance operations.

![Tab 3 - 3D Inspection](./assets/3D.png)

---

## ✨ Key Features

- **Predictive Risk Scoring:** ML Model (`Scikit-Learn`) forecasting delay probabilities based on lead time, ordered quantities, fill rates, supplier history, and quality incidents.
- **AI Supply Chain Copilot:** Integrated LLaMA-3.3-70B (via Groq API) acting as a domain-expert decision assistant with structured action plans.
- **2D Warehouse Digital Twin:** Interactive Plotly map visualizing warehouse rack occupancy and criticality at Casablanca CMN Hub.
- **3D Aeronautical Viewer:** Embedded 3D model inspection for aircraft components (gLFT / Sketchfab integration).
- **Fully Containerized:** Packaged with Docker for seamless deployment across local and cloud environments.
- **Cloud Ready:** Containerized with Docker, ready for AWS deployment (EC2 / App Runner / ECS).

---

## 🏗️ Architecture

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        Streamlit Cockpit UI                            │
├────────────────────────┬───────────────────────┬───────────────────────┤
│ Tab 1: ML & AI Agent   │ Tab 2: 2D Digital Twin│ Tab 3: 3D Inspection  │
└───────────┬────────────┴───────────┬───────────┴───────────┬───────────┘
            │                        │                       │
            ▼                        ▼                       ▼
   [ Scikit-Learn ML ]      [ Plotly Spatial Map ]    [ 3D / WebGL Viewer ]
   [ Groq LLaMA-3 Agent]    (Warehouse Racks CMN)     (Boeing 787 Models)
            │
            ▼
   [ Docker Container ] ──► [ AWS Cloud Deployment ]
```

---

## 🚀 Quickstart Guide

### Prerequisites
- Docker Desktop installed and running.
- A free Groq API Key.

### Running with Docker (Recommended)

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/cattcookies70-sudo/MRO-Supply-Twin-AI.git](https://github.com/cattcookies70-sudo/MRO-Supply-Twin-AI.git)
   cd MRO-Supply-Twin-AI
   ```

2. **Build the Docker Image:**
   ```bash
   docker build -t supplytwin-mro:v1 .
   ```

3. **Run the Container:**
   ```bash
   docker run -d -p 8501:8501 -e GROQ_API_KEY="your_groq_api_key_here" --name supplytwin_app supplytwin-mro:v1
   ```

4. Open `http://localhost:8501` in your browser.

---

## 📂 Project Structure

```text
.
├── .devcontainer/           # Dev Container configuration
├── assets/                  # Dashboard screenshots & media
│   ├── dashboard.png
│   ├── 2D.png
│   └── 3D.png
├── data/                    # Processed MRO datasets
├── models/                  # Trained ML models (.pkl)
├── notebooks/               # Data science & LLM development notebooks
├── .gitignore               # Git ignore rules
├── Dockerfile               # Docker build instructions
├── docker-compose.yml       # Multi-container orchestrator configuration
├── README.md                # Project documentation
├── app.py                   # Main Streamlit Cockpit Application
├── requirements.txt         # Python dependencies
└── test_groq.py             # Script for testing Groq API connection
```

---

## 🎓 Author
Developed as an Engineering Project at **École Centrale Casablanca**.
