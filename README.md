# Déploiement : Prédiction du Prix de Vente d'une Voiture (Regression Doc 2)

Cette application Streamlit permet d'estimer la valeur marchande de revente d'un véhicule d'occasion (`Selling_Price`, en k$) à partir de ses caractéristiques techniques et d'usage.

## Modèle retenu et artefacts
- **Modèle final :** `Pipeline([('scaler', RobustScaler()), ('regressor', RandomForestRegressor(max_depth=14, n_estimators=80))])` sauvegardé dans `pipe_from_grid.joblib`. Modèle sélectionné pour son meilleur $R^2 = 0.88$ sur l'ensemble de validation et son excellente stabilité.
- **Encodeurs catégoriels :** Liste de 3 `LabelEncoder` sauvegardée dans `encoders.joblib` :
  1. `Fuel_Type` : `['CNG', 'Diesel', 'Petrol']`
  2. `Seller_Type` : `['Dealer', 'Individual']`
  3. `Transmission` : `['Automatic', 'Manual']`

## Variables en entrée
1. `Kms_Driven` : Kilométrage total parcouru par le véhicule.
2. `Present_Price` : Prix neuf du véhicule en concession (k$).
3. `Age` : Âge du véhicule en années.
4. `Fuel_Type` : Type de motorisation/carburant.
5. `Seller_Type` : Vendeur particulier ou professionnel.
6. `Transmission` : Boîte de vitesses automatique ou manuelle.

## Lancement en local
```bash
cd "Rendu/Supervised/Regression/Doc 2/Deployment"
streamlit run app.py
```
