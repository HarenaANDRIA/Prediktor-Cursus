import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, f1_score
from xgboost import XGBClassifier

# 1. Chargement du dataset nettoyé
df = pd.read_csv('data/processed/dataset_cleaned.csv', sep=';', decimal=',')
feature_cols = [col for col in df.columns if col != "filiere_recommandee"]

for col in feature_cols:
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.'), errors='coerce')

X = df[feature_cols]
y_raw = df["filiere_recommandee"]

label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y_raw)

os.makedirs('models', exist_ok=True)
joblib.dump(label_encoder, 'models/label_encoder.joblib')

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# ---------------------------------------------------------------------------
# 2. Deux candidats : XGBoost et RandomForest, chacun avec sa propre recherche
#    d'hyperparamètres. Celui qui obtient le meilleur F1-Score macro (validation
#    croisée) est conservé pour l'évaluation finale et la sauvegarde.
# ---------------------------------------------------------------------------
candidates = {
    "XGBoost": {
        "pipeline": Pipeline([
            ('scaler', StandardScaler()),
            ('classifier', XGBClassifier(random_state=42, eval_metric='mlogloss'))
        ]),
        "param_grid": {
            'classifier__n_estimators': [100, 150, 200],
            'classifier__max_depth': [4, 6, 8],
            'classifier__learning_rate': [0.05, 0.1],
        },
    },
    "RandomForest": {
        "pipeline": Pipeline([
            ('scaler', StandardScaler()),
            ('classifier', RandomForestClassifier(random_state=42))
        ]),
        "param_grid": {
            'classifier__n_estimators': [200, 300, 400],
            'classifier__max_depth': [None, 10, 20],
            'classifier__min_samples_split': [2, 5],
        },
    },
}

results = {}
for name, cfg in candidates.items():
    print(f"\n🔎 Entraînement et recherche d'hyperparamètres : {name}")
    grid_search = GridSearchCV(
        estimator=cfg["pipeline"],
        param_grid=cfg["param_grid"],
        cv=cv,
        scoring='f1_macro',
        n_jobs=-1
    )
    grid_search.fit(X_train, y_train)
    results[name] = grid_search
    print(f"   → Meilleur F1-Score macro (CV) pour {name} : {grid_search.best_score_ * 100:.2f}%")
    print(f"   → Meilleurs paramètres : {grid_search.best_params_}")

# 3. Sélection du meilleur modèle selon le F1-Score macro de validation croisée
best_model_name = max(results, key=lambda name: results[name].best_score_)
best_grid_search = results[best_model_name]
best_pipeline = best_grid_search.best_estimator_

print(f"\n🏆 Modèle retenu : {best_model_name} (F1 macro CV = {best_grid_search.best_score_ * 100:.2f}%)")

# 4. Évaluation finale sur le jeu de test
y_pred = best_pipeline.predict(X_test)
test_f1 = f1_score(y_test, y_pred, average='macro')
print(f"🎯 F1-Score Macro Test ({best_model_name}) : {test_f1 * 100:.2f}%")
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

# 5. Sauvegarde du meilleur pipeline uniquement
joblib.dump(best_pipeline, 'models/best_pipeline_filiere.joblib')
with open('models/model_report.txt', 'w', encoding='utf-8') as f:
    f.write(f"Modèle retenu : {best_model_name}\n")
    f.write(f"F1-Score macro (CV) : {best_grid_search.best_score_ * 100:.2f}%\n")
    f.write(f"F1-Score macro (Test) : {test_f1 * 100:.2f}%\n")
    f.write(f"Meilleurs paramètres : {best_grid_search.best_params_}\n\n")
    f.write(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

print(f"✅ Pipeline réentraîné avec les {len(feature_cols)} matières et {len(label_encoder.classes_)} filières.")
print(f"✅ Meilleur modèle ({best_model_name}) sauvegardé dans models/best_pipeline_filiere.joblib")
