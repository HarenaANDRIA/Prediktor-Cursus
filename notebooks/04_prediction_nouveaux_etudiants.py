# ==============================================================================
# NOTEBOOK 4 : PREDICTION VIA PIPELINE SAUVEGARDÉ (CORRIGÉ)
# ==============================================================================

import pandas as pd
import numpy as np
import joblib

# 1. Chargement du Pipeline et du LabelEncoder
pipeline = joblib.load('models/best_pipeline_filiere.joblib')
label_encoder = joblib.load('models/label_encoder.joblib')

# 2. Données brutes de test
nouveaux_etudiants = pd.DataFrame([
    {
        "mathematiques": 17.5, "physique_et_chimie": 16.0,
        "science_de_la_vie_et_de_la_terre": 12.0, "francais": 10.0,
        "anglais": 14.5, "philosophie": 9.0,
        "histoire_et_geographie": 11.0, "test_psychotechnique": 15.0
    },
    {
        "mathematiques": 8.0, "physique_et_chimie": 9.5,
        "science_de_la_vie_et_de_la_terre": 10.0, "francais": 16.0,
        "anglais": 17.0, "philosophie": 15.5,
        "histoire_et_geographie": 14.0, "test_psychotechnique": 12.0
    }
])

# On récupère l'ordre exact des colonnes utilisé pendant l'entraînement
expected_features = pipeline.feature_names_in_
nouveaux_etudiants = nouveaux_etudiants[expected_features]

# 4. Prédiction via le Pipeline
probabilites = pipeline.predict_proba(nouveaux_etudiants)
classes_noms = label_encoder.classes_

for i, student in nouveaux_etudiants.iterrows():
    print(f"==================================================")
    print(f"🎓 PROFIL ÉTUDIANT n°{i+1}")
    print(f"Maths: {student['mathematiques']} | Physique: {student['physique_et_chimie']} | Français: {student['francais']} | Anglais: {student['anglais']}")
    print(f"--------------------------------------------------")
    
    top3_indices = np.argsort(probabilites[i])[::-1][:3]
    confiance_cumulee = 0
    
    for rank, class_idx in enumerate(top3_indices, 1):
        filiere = classes_noms[class_idx].replace('_', ' ').title()
        proba = probabilites[i][class_idx] * 100
        confiance_cumulee += proba
        
        médaille = "🥇" if rank == 1 else ("🥈" if rank == 2 else "🥉")
        print(f"  {médaille} Option {rank} : {filiere:<40} ({proba:.1f}%)")
    
    print(f"\n📊 Confiance cumulée (Top 3) : {confiance_cumulee:.1f}%\n")