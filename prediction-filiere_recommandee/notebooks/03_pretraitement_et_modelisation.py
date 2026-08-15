# ==============================================================================
# NOTEBOOK 3 : PIPELINE PROFESSIONNEL ET RIGUEUR SCIENTIFIQUE
# Objectif : Zéro Data Leakage, Cross-Validation, Metrics Robustes & Explicabilité
# ==============================================================================

import os
import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix, f1_score
from xgboost import XGBClassifier

# ------------------------------------------------------------------------------
# 1. Chargement et Préparation des Données
# ------------------------------------------------------------------------------
df = pd.read_csv('data/processed/dataset_cleaned.csv', sep=';', decimal=',')
feature_cols = [col for col in df.columns if col != "filiere_recommandee"]

for col in feature_cols:
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.'), errors='coerce')
df = df.dropna()

X = df[feature_cols]
y_raw = df["filiere_recommandee"]

# Encodage de la variable cible
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y_raw)

os.makedirs('models', exist_ok=True)
joblib.dump(label_encoder, 'models/label_encoder.joblib')

# ------------------------------------------------------------------------------
# 2. Séparation Train / Test (Sans aucun prétraitement préalable)
# ------------------------------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ------------------------------------------------------------------------------
# 3. Création du Pipeline (Élimination du Data Leakage)
# ------------------------------------------------------------------------------
# Le scaler sera ajusté UNIQUEMENT sur le fold d'entraînement à chaque étape
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', XGBClassifier(random_state=42, eval_metric='mlogloss'))
])

# ------------------------------------------------------------------------------
# 4. Recherche par Grille avec Validation Croisée (GridSearchCV)
# ------------------------------------------------------------------------------
print("--- Optimisation par Validation Croisée (5-Fold Stratified) ---")

# Définition de la grille d'hyperparamètres
param_grid = {
    'classifier__n_estimators': [100, 150, 200],
    'classifier__max_depth': [4, 6, 8],
    'classifier__learning_rate': [0.01, 0.05, 0.1],
    'classifier__subsample': [0.8, 1.0]
}

# StratifiedKFold préserve le pourcentage d'échantillons de chaque classe
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

grid_search = GridSearchCV(
    estimator=pipeline,
    param_grid=param_grid,
    cv=cv,
    scoring='f1_macro', # Optimisation sur le Macro F1 au lieu de l'Accuracy
    n_jobs=-1,
    verbose=1
)

grid_search.fit(X_train, y_train)

best_pipeline = grid_search.best_estimator_
print(f"\nMeilleurs hyperparamètres : {grid_search.best_params_}")
print(f"Meilleur F1-Score Macro en validation croisée : {grid_search.best_score_:.4f}")

# ------------------------------------------------------------------------------
# 5. Évaluation Finale Rigoureuse sur le Jeu de Test
# ------------------------------------------------------------------------------
print("\n--- ÉVALUATION SUR LE JEU DE TEST (DONNÉESINÉDITES) ---")
y_pred = best_pipeline.predict(X_test)

macro_f1 = f1_score(y_test, y_pred, average='macro')
weighted_f1 = f1_score(y_test, y_pred, average='weighted')

print(f"🎯 F1-Score Macro (Test)    : {macro_f1 * 100:.2f}%")
print(f"🎯 F1-Score Weighted (Test) : {weighted_f1 * 100:.2f}%")

print("\nRapport de classification détaillé :")
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

# ------------------------------------------------------------------------------
# 6. Explicabilité : Importance des Matériels (Feature Importance)
# ------------------------------------------------------------------------------
print("\n--- EXPLICABILITÉ DU MODÈLE (Importance des caractéristiques) ---")
xgb_model = best_pipeline.named_steps['classifier']
importances = xgb_model.feature_importances_

feature_importance_df = pd.DataFrame({
    'Matiere': feature_cols,
    'Importance (%)': importances * 100
}).sort_values(by='Importance (%)', ascending=False)

print(feature_importance_df.to_string(index=False))

# ------------------------------------------------------------------------------
# 7. Sauvegarde du Pipeline Complet
# ------------------------------------------------------------------------------
joblib.dump(best_pipeline, 'models/best_pipeline_filiere.joblib')
print("\n[OK] Pipeline complet (Scaler + XGBoost) sauvegardé avec succès.")