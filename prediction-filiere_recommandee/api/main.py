import os
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="API Orientation Multi-Séries ML", version="3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Pointer vers le dossier models/ situé à la racine du projet (en dehors du dossier api/)
MODELS_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "models"))

# Cartographie explicite des matières par série au cas où feature_names_in_ n'est pas disponible
SERIES_FEATURES = {
    'aucune': [
        'mathematiques', 'physique', 'chimie', 'francais', 'histoire_et_geographie',
        'philosophie', 'anglais', 'test_psychotechnique', 'science_de_la_vie_et_de_la_terre',
        'statistiques_et_probabilites'
    ],
    'scientifique': [
        'mathematiques', 'physique', 'chimie', 'francais', 'histoire_et_geographie',
        'philosophie', 'anglais', 'test_psychotechnique', 'science_de_la_vie_et_de_la_terre',
        'statistiques_et_probabilites'
    ],
    'litteraire': [
        'francais', 'histoire_et_geographie', 'philosophie', 'anglais',
        'test_psychotechnique', 'statistiques_et_probabilites'
    ],
    'ose': [
        'mathematiques', 'francais', 'histoire_et_geographie', 'philosophie',
        'anglais', 'test_psychotechnique', 'statistiques_et_probabilites'
    ]
}

# Dictionnaires pour charger les modèles et label encoders de chaque série
pipelines_filiere = {}
encoders_filiere = {}

series_keys = ['aucune', 'scientifique', 'litteraire', 'ose']

for s in series_keys:
    p_path = os.path.join(MODELS_DIR, f"best_pipeline_filiere_{s}.joblib")
    e_path = os.path.join(MODELS_DIR, f"label_encoder_filiere_{s}.joblib")
    if os.path.exists(p_path) and os.path.exists(e_path):
        try:
            pipelines_filiere[s] = joblib.load(p_path)
            encoders_filiere[s] = joblib.load(e_path)
            print(f"✅ Modèle Filière Série {s.upper()} chargé depuis {MODELS_DIR}")
        except Exception as err:
            print(f"⚠️ Erreur chargement Série {s}: {err}")
    else:
        print(f"⚠️ Modèles introuvables pour la série {s} dans {MODELS_DIR}")

# Chargement du modèle de branche
pipeline_branch_path = os.path.join(MODELS_DIR, "best_pipeline_branch.joblib")
encoder_branch_path = os.path.join(MODELS_DIR, "label_encoder_branch.joblib")

pipeline_branch = None
label_encoder_branch = None

try:
    if os.path.exists(pipeline_branch_path) and os.path.exists(encoder_branch_path):
        pipeline_branch = joblib.load(pipeline_branch_path)
        label_encoder_branch = joblib.load(encoder_branch_path)
        print(f"✅ Modèle Branche Universitaire chargé depuis {MODELS_DIR}")
    else:
        print(f"⚠️ Modèle de branche introuvable dans {MODELS_DIR}")
except Exception as e:
    print(f"⚠️ Warning Modèle Branche: {e}")


class NotesEtudiantInput(BaseModel):
    serie: str = "aucune"
    mathematiques: Optional[float] = 10.0
    physique: Optional[float] = 10.0
    chimie: Optional[float] = 10.0
    francais: Optional[float] = 10.0
    histoire_et_geographie: Optional[float] = 10.0
    philosophie: Optional[float] = 10.0
    anglais: Optional[float] = 10.0
    test_psychotechnique: Optional[float] = 10.0
    science_de_la_vie_et_de_la_terre: Optional[float] = 10.0
    statistiques_et_probabilites: Optional[float] = 10.0


class BranchInput(BaseModel):
    filiere: str
    notes_modules: Dict[str, float]


@app.post("/predict")
def predict(data: NotesEtudiantInput):
    try:
        serie_key = (data.serie or "aucune").lower()
        if serie_key not in pipelines_filiere or serie_key not in encoders_filiere:
            serie_key = "aucune"

        pipeline = pipelines_filiere.get(serie_key)
        encoder = encoders_filiere.get(serie_key)

        if not pipeline or not encoder:
            raise HTTPException(
                status_code=500,
                detail=f"Modèle pour la série '{serie_key}' non chargé. Vérifiez l'emplacement '{MODELS_DIR}'."
            )

        # 1. Traitement des données d'entrée et remplacement des None par 10.0
        input_dict = data.model_dump() if hasattr(data, "model_dump") else data.dict()
        input_dict.pop('serie', None)

        for k, v in input_dict.items():
            if v is None:
                input_dict[k] = 10.0

        df_input = pd.DataFrame([input_dict])

        # 2. Récupération des features attendues
        if hasattr(pipeline, "feature_names_in_"):
            expected_cols = list(pipeline.feature_names_in_)
        elif hasattr(pipeline, "named_steps") and hasattr(pipeline.named_steps.get('classifier'), "feature_names_in_"):
            expected_cols = list(pipeline.named_steps['classifier'].feature_names_in_)
        else:
            expected_cols = SERIES_FEATURES.get(serie_key, SERIES_FEATURES['aucune'])

        # 3. Réalignement strict du DataFrame
        for col in expected_cols:
            if col not in df_input.columns:
                df_input[col] = 10.0

        df_input = df_input[expected_cols]

        # 4. Calcul des prédictions
        probabilities = pipeline.predict_proba(df_input)[0]
        classes_noms = encoder.classes_

        top3_indices = np.argsort(probabilities)[::-1][:3]

        recommandations = []
        for rank, idx in enumerate(top3_indices, 1):
            recommandations.append({
                "rang": rank,
                "filiere": str(classes_noms[idx]),
                "probabilite": round(float(probabilities[idx]) * 100, 1)
            })

        return {"recommandations": recommandations, "serie_utilisee": serie_key}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur prédiction filière : {str(e)}")


@app.post("/predict-branch")
def predict_branch(data: BranchInput):
    try:
        if not pipeline_branch or not label_encoder_branch:
            raise HTTPException(status_code=500, detail="Modèle de branche non disponible.")

        data_dict = data.notes_modules.copy()
        data_dict['filiere'] = data.filiere
        df_input = pd.DataFrame([data_dict])
        df_input = pd.get_dummies(df_input, columns=['filiere'])

        if hasattr(pipeline_branch, "feature_names_in_"):
            expected_cols = list(pipeline_branch.feature_names_in_)
            for col in expected_cols:
                if col not in df_input.columns:
                    if col.startswith("filiere_"):
                        df_input[col] = 0
                    else:
                        df_input[col] = 9.5
            df_input = df_input[expected_cols]

        probabilities = pipeline_branch.predict_proba(df_input)[0]
        classes_noms = label_encoder_branch.classes_

        top3_indices = np.argsort(probabilities)[::-1][:3]

        recommandations = []
        for rank, idx in enumerate(top3_indices, 1):
            recommandations.append({
                "rang": rank,
                "branche": str(classes_noms[idx]),
                "probabilite": round(float(probabilities[idx]) * 100, 1)
            })

        return {"recommandations": recommandations}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur prédiction branche : {str(e)}")