"""
Application Streamlit — Prédiction du prix de vente d'un véhicule (Regression Doc 2)
Modèle retenu : RandomForestRegressor dans un Pipeline avec RobustScaler
Lancement en local : streamlit run app.py
"""

import os
import joblib
import numpy as np
import streamlit as st

# ----------------------------------------------------------------------
# Configuration de la page
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Car Selling Price Prediction",
    page_icon="🚗",
    layout="centered",
)

DESCRIPTION = (
    "Cette application permet d'estimer le prix de vente d'un véhicule d'occasion (en k$) "
    "à partir du kilométrage, du prix d'origine neuf (Present Price), du type de carburant, "
    "du type de vendeur, de la boîte de transmission et de l'âge du véhicule."
)

NOTE_PREPROCESSING = (
    "⚠️ **Remarque méthodologique :** Ce modèle a été entraîné sur un jeu de données dont les prix "
    "ont été plafonnés par l'imputation KNN réalisée lors de la préparation des données du cours. "
    "Par conséquent, les prédictions sont peu fiables pour les véhicules très haut de gamme ou de luxe."
)

# ----------------------------------------------------------------------
# Chargement des artefacts (mis en cache)
# ----------------------------------------------------------------------
@st.cache_resource
def load_artifacts():
    base_dir = os.path.dirname(__file__)
    encoders = joblib.load(os.path.join(base_dir, "encoders.joblib"))
    pipe_from_grid = joblib.load(os.path.join(base_dir, "pipe_from_grid.joblib"))
    return encoders, pipe_from_grid


encoders, pipe_from_grid = load_artifacts()

# ----------------------------------------------------------------------
# Fonction de prédiction simple
# ----------------------------------------------------------------------
def predict_car_price(kms_driven, present_price, fuel_type, seller_type, transmission, age):
    # Encodage des caractéristiques catégorielles avec les encodeurs sauvegardés
    fuel_enc = encoders[0].transform([fuel_type])[0]
    seller_enc = encoders[1].transform([seller_type])[0]
    trans_enc = encoders[2].transform([transmission])[0]
    
    # Vecteur d'entrée structuré dans l'ordre exact du dataset
    raw_vector = np.array([[kms_driven, present_price, fuel_enc, seller_enc, trans_enc, age]])
    
    # Prédiction via le Pipeline (RobustScaler + RandomForestRegressor)
    y_pred = pipe_from_grid.predict(raw_vector)[0]
    
    # Prix strictement positif
    y_pred_positive = max(0.05, float(y_pred))
    return round(y_pred_positive, 2)


# ----------------------------------------------------------------------
# Interface utilisateur
# ----------------------------------------------------------------------
st.title("🚗 Car Selling Price Prediction")
st.write(DESCRIPTION)
st.info(NOTE_PREPROCESSING)

with st.form("form_single_car_prediction"):
    col1, col2 = st.columns(2)
    with col1:
        kms_driven = st.number_input(
            "Kms Driven (Kilométrage parcouru)",
            min_value=0.0,
            max_value=500000.0,
            value=27000.0,
            step=1000.0,
            format="%.1f",
        )
        present_price = st.number_input(
            "Present Price (Prix neuf indicatif, en k$)",
            min_value=0.1,
            max_value=100.0,
            value=5.59,
            step=0.5,
            format="%.2f",
        )
        age = st.number_input(
            "Age (Âge du véhicule en années)",
            min_value=0.0,
            max_value=40.0,
            value=6.0,
            step=1.0,
            format="%.1f",
        )
    with col2:
        fuel_type = st.selectbox(
            "Fuel Type (Carburant)",
            options=list(encoders[0].classes_),
        )
        seller_type = st.selectbox(
            "Seller Type (Type de vendeur)",
            options=list(encoders[1].classes_),
        )
        transmission = st.selectbox(
            "Transmission (Boîte de vitesse)",
            options=list(encoders[2].classes_),
        )

    submit_btn = st.form_submit_button("Prédire le prix", type="primary")

if submit_btn:
    try:
        prix_estime = predict_car_price(
            kms_driven, present_price, fuel_type, seller_type, transmission, age
        )
        st.success(f"💰 **Prix de vente estimé : {prix_estime} k$**")
    except Exception as e:
        st.error(f"Erreur lors de la prédiction : {e}")
