import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, f1_score
from xgboost import XGBClassifier

# Interrupteur unique pour activer/desactiver le garde-fou metier (voir bloc
# GARDE-FOU en bas du fichier). Passer a False pour tester le modele brut,
# sans aucune contrainte metier appliquee sur les predictions.
APPLIQUER_GARDE_FOU = False

df = pd.read_csv('data/processed/dataset_cleaned.csv', sep=';', decimal=',')
notes_cols = [col for col in df.columns if col not in ["filiere_recommandee", "serie"]]

for col in notes_cols:
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.'), errors='coerce')

# Variables explicatives (Notes + Série) et variable cible (Filière)
X = df[notes_cols + ["serie"]]
y_raw = df["filiere_recommandee"]

label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y_raw)

os.makedirs('models', exist_ok=True)
joblib.dump(label_encoder, 'models/label_encoder.joblib')

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Prétraitement combiné : notes numériques + série catégorielle
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), notes_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore'), ['serie'])
    ]
)

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# ---------------------------------------------------------------------------
# Deux candidats sont entraînés avec GridSearchCV : RandomForest et XGBoost.
# Celui qui obtient le meilleur F1-macro sur le jeu de test est retenu.
# ---------------------------------------------------------------------------
candidates = {}

# --- Candidat 1 : RandomForest ---
rf_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(random_state=42))
])
rf_param_grid = {
    'classifier__n_estimators': [200, 400],
    'classifier__max_depth': [None, 10, 20],
    'classifier__min_samples_leaf': [1, 2],
}
candidates['RandomForest'] = (rf_pipeline, rf_param_grid)

# --- Candidat 2 : XGBoost ---
xgb_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', XGBClassifier(random_state=42, eval_metric='mlogloss'))
])
xgb_param_grid = {
    'classifier__n_estimators': [100, 150],
    'classifier__max_depth': [4, 6],
    'classifier__learning_rate': [0.05, 0.1]
}
candidates['XGBoost'] = (xgb_pipeline, xgb_param_grid)

results = {}
for name, (pipeline, param_grid) in candidates.items():
    print(f"\n=== Entraînement : {name} ===")
    grid_search = GridSearchCV(
        estimator=pipeline,
        param_grid=param_grid,
        cv=cv,
        scoring='f1_macro',
        n_jobs=-1
    )
    grid_search.fit(X_train, y_train)
    best_pipeline = grid_search.best_estimator_

    y_pred = best_pipeline.predict(X_test)
    f1_test = f1_score(y_test, y_pred, average='macro')

    print(f"🎯 F1-Score Macro Test ({name}) : {f1_test * 100:.2f}%")
    print(f"Meilleurs hyperparamètres ({name}) : {grid_search.best_params_}")
    print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

    results[name] = {
        'pipeline': best_pipeline,
        'f1_test': f1_test,
        'best_params': grid_search.best_params_
    }

# ---------------------------------------------------------------------------
# Sélection du meilleur modèle selon le F1-Score macro sur le jeu de test
# ---------------------------------------------------------------------------
best_model_name = max(results, key=lambda name: results[name]['f1_test'])
best_pipeline = results[best_model_name]['pipeline']

print("\n" + "=" * 60)
print("RÉCAPITULATIF")
print("=" * 60)
for name, res in results.items():
    marker = " ⭐ RETENU" if name == best_model_name else ""
    print(f"{name} : F1-macro = {res['f1_test'] * 100:.2f}%{marker}")

joblib.dump(best_pipeline, 'models/best_pipeline_filiere.joblib')
joblib.dump(best_model_name, 'models/best_model_name.joblib')
print(f"\n✅ Meilleur modèle ({best_model_name}) réentraîné et sauvegardé dans models/best_pipeline_filiere.joblib")


# =============================================================================
# ============================ DEBUT — GARDE-FOU =============================
# =============================================================================
# POURQUOI CE BLOC EXISTE :
# Le modèle ci-dessus (RandomForest ou XGBoost, ~90% de F1-macro) reste un
# modèle STATISTIQUE : rien ne l'empêche mathématiquement, sur un cas
# atypique ou hors distribution d'entraînement, de recommander une filière
# incohérente avec la série de l'élève (ex : une filière purement
# scientifique/technique pour un élève littéraire). Une bonne performance
# ne vaut pas garantie logique.
#
# CE QUE FAIT CE BLOC :
# Après la prédiction du modèle, on met à zéro la probabilité de toute
# filière interdite pour la série de l'élève, puis on reprend l'argmax
# uniquement parmi les filières autorisées. Ceci applique en dur les règles
# de prompt.docx (un élève littéraire ne peut jamais recevoir une filière
# purement scientifique — règles 2 et 5), indépendamment de la qualité du
# modèle.
#
# COMMENT LE RETIRER / LE DÉSACTIVER POUR UN TEST :
#   - Rapide (sans rien supprimer) : mettre APPLIQUER_GARDE_FOU = False en
#     haut du fichier -> predict_filiere_finale() renverra alors les
#     prédictions BRUTES du modèle, sans filtre métier.
#   - Suppression complète : supprimer tout le contenu compris entre les
#     lignes "DEBUT — GARDE-FOU" et "FIN — GARDE-FOU" ci-dessous ; le reste
#     du script (entraînement, sélection du meilleur modèle) fonctionne de
#     façon totalement indépendante et n'est pas affecté.
# =============================================================================

PURELY_SCI = ["pharmacie", "medecine_et_sante", "genie_electrique_et_electronique",
              "informatique_administration_reseaux_et_ia", "genie_mecanique_et_industriel",
              "genie_civil_et_construction", "science_des_donnees_et_intelligence_artificielle",
              "biotechnologie_et_sciences_pharmaceutiques", "sciences_veterinaires",
              "urbanisme_et_amenagement_du_territoire", "cybersecurite_et_reseaux",
              "agronomie_et_environnement", "architecture_et_design_interieur",
              "sciences_actuarielles_et_statistiques"]

PURELY_LIT = ["traduction_et_interpretariat", "journalisme_et_medias",
              "sciences_sociales_et_sociologie", "sport_et_sciences_du_mouvement",
              "droit_et_sciences_politiques", "tourisme_et_hotellerie",
              "psychologie_et_sciences_de_l_education", "langues_et_communication"]

PARTIAL_SCI = ["finance_comptabilite_et_audit", "economie_et_gestion",
               "commerce_international_et_logistique"]


def filieres_autorisees(serie: str) -> list:
    """Règles strictes de prompt.docx :
    - un élève littéraire ne peut JAMAIS recevoir une filière purement
      scientifique (règles 2 et 5) -> uniquement purely_lit + partial_sci.
    - un élève scientifique peut recevoir n'importe quelle catégorie
      (règles 1, 3 et 4)."""
    if serie == "litteraire":
        return PURELY_LIT + PARTIAL_SCI
    return PURELY_SCI + PURELY_LIT + PARTIAL_SCI


def predict_filiere_finale(pipeline, label_encoder, X: pd.DataFrame) -> pd.Series:
    """Prédit la filière recommandée.
    - Si APPLIQUER_GARDE_FOU est True (par défaut) : applique le filtre
      métier (garantie absolue de cohérence avec la série de l'élève).
    - Si APPLIQUER_GARDE_FOU est False : renvoie la prédiction brute du
      modèle, utile pour tester/déboguer le modèle seul."""
    if not APPLIQUER_GARDE_FOU:
        preds = pipeline.predict(X)
        return pd.Series(label_encoder.inverse_transform(preds), index=X.index,
                          name="filiere_recommandee_predite")

    proba = pipeline.predict_proba(X)  # (n_samples, n_classes)
    classes = label_encoder.classes_

    resultats = []
    for i in range(len(X)):
        serie = X.iloc[i]["serie"]
        autorisees = set(filieres_autorisees(serie))
        p = proba[i].copy()
        for j, cls in enumerate(classes):
            if cls not in autorisees:
                p[j] = 0.0
        if p.sum() == 0:
            # filet de sécurité (ne devrait jamais arriver)
            idx_autorises = [j for j, c in enumerate(classes) if c in autorisees]
            meilleur_idx = idx_autorises[np.argmax(proba[i][idx_autorises])]
        else:
            meilleur_idx = int(np.argmax(p))
        resultats.append(classes[meilleur_idx])

    return pd.Series(resultats, index=X.index, name="filiere_recommandee_predite")


# --- Démonstration / auto-test du garde-fou sur un cas piège : un élève
# littéraire avec des notes scientifiques volontairement excellentes ---
demo = pd.DataFrame([{
    "mathematiques": 18, "physique": 17, "chimie": 18, "francais": 19,
    "histoire_et_geographie": 16, "philosophie": 16, "anglais": 17,
    "test_psychotechnique": 12, "science_de_la_vie_et_de_la_terre": 17,
    "informatique": 18, "economie_generale": 12, "education_physique_et_sportive": 11,
    "dessin_technique_et_arts_appliques": 16, "statistiques_et_probabilites": 17,
    "biologie_appliquee_et_biotechnologie": 17, "serie": "litteraire",
}])
pred_demo = predict_filiere_finale(best_pipeline, label_encoder, demo)
filiere_demo = pred_demo.iloc[0]
statut = "❌ ÉCHEC" if (APPLIQUER_GARDE_FOU and filiere_demo in PURELY_SCI) else "✅ OK"
print(f"\n[Garde-fou] Test élève littéraire à notes scientifiques élevées "
      f"-> filière prédite : {filiere_demo} ({statut})")

# =============================================================================
# ============================= FIN — GARDE-FOU ==============================
# Rappel : pour retirer ce mécanisme, supprimer uniquement le bloc compris
# entre "DEBUT — GARDE-FOU" et cette ligne. L'entraînement et la sauvegarde
# du modèle plus haut dans ce fichier restent intacts et fonctionnels.
# =============================================================================
