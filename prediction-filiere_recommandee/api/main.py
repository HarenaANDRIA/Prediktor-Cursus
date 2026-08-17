import os
import joblib
import numpy as np
import pandas as pd
from typing import Dict
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="API Orientation ML", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 1. Chargement du modèle Filières Post-Bac
pipeline_filiere_path = os.path.join(BASE_DIR, "models", "best_pipeline_filiere.joblib")
encoder_filiere_path = os.path.join(BASE_DIR, "models", "label_encoder.joblib")

# 2. Chargement du modèle Branches Universitaires
pipeline_branch_path = os.path.join(BASE_DIR, "models", "best_pipeline_branch.joblib")
encoder_branch_path = os.path.join(BASE_DIR, "models", "label_encoder_branch.joblib")

pipeline = None
label_encoder = None
pipeline_branch = None
label_encoder_branch = None

try:
    if os.path.exists(pipeline_filiere_path) and os.path.exists(encoder_filiere_path):
        pipeline = joblib.load(pipeline_filiere_path)
        label_encoder = joblib.load(encoder_filiere_path)
except Exception as e:
    print(f"⚠️ Warning Modèle Filière: {e}")

try:
    if os.path.exists(pipeline_branch_path) and os.path.exists(encoder_branch_path):
        pipeline_branch = joblib.load(pipeline_branch_path)
        label_encoder_branch = joblib.load(encoder_branch_path)
except Exception as e:
    print(f"⚠️ Warning Modèle Branche: {e}")


class NotesEtudiant(BaseModel):
    mathematiques: float = Field(..., ge=0, le=20)
    physique: float = Field(..., ge=0, le=20)
    chimie: float = Field(..., ge=0, le=20)
    francais: float = Field(..., ge=0, le=20)
    histoire_et_geographie: float = Field(..., ge=0, le=20)
    philosophie: float = Field(..., ge=0, le=20)
    anglais: float = Field(..., ge=0, le=20)
    test_psychotechnique: float = Field(..., ge=0, le=20)
    science_de_la_vie_et_de_la_terre: float = Field(..., ge=0, le=20)
    statistiques_et_probabilites: float = Field(..., ge=0, le=20)


class BranchInput(BaseModel):
    filiere: str
    notes_modules: Dict[str, float]


@app.post("/predict")
def predict(notes: NotesEtudiant):
    try:
        if not pipeline or not label_encoder:
            raise HTTPException(status_code=500, detail="Modèle de filière non disponible.")

        data_dict = notes.model_dump() if hasattr(notes, "model_dump") else notes.dict()
        df_input = pd.DataFrame([data_dict])

        if hasattr(pipeline, "feature_names_in_"):
            df_input = df_input[pipeline.feature_names_in_]

        probabilities = pipeline.predict_proba(df_input)[0]
        classes_noms = label_encoder.classes_
        
        top3_indices = np.argsort(probabilities)[::-1][:3]

        recommandations = []
        for rank, idx in enumerate(top3_indices, 1):
            recommandations.append({
                "rang": rank,
                "filiere": classes_noms[idx].replace("_", " ").title(),
                "probabilite": round(float(probabilities[idx]) * 100, 1)
            })

        return {"recommandations": recommandations}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la prédiction filière : {str(e)}")


@app.post("/predict-branch")
def predict_branch(data: BranchInput):
    try:
        if not pipeline_branch or not label_encoder_branch:
            raise HTTPException(status_code=500, detail="Modèle de branche non disponible.")

        # 1. Construction de la ligne d'entrée avec la filière et les notes envoyées
        data_dict = data.notes_modules.copy()
        data_dict['filiere'] = data.filiere
        df_input = pd.DataFrame([data_dict])

        # 2. Encodage One-Hot de la filière
        df_input = pd.get_dummies(df_input, columns=['filiere'])

        # 3. Alignement exact sur les colonnes attendues par le pipeline entraîné
        if hasattr(pipeline_branch, "feature_names_in_"):
            expected_cols = pipeline_branch.feature_names_in_
            for col in expected_cols:
                if col not in df_input.columns:
                    # Si c'est un module non renseigné -> valeur baseline 9.5
                    # Si c'est une colonne 'filiere_xxx' non active -> 0 (False)
                    if col.startswith("filiere_"):
                        df_input[col] = 0
                    else:
                        df_input[col] = 9.5

            # Re-ordonner les colonnes pour correspondre au modèle
            df_input = df_input[expected_cols]

        # 4. Prédiction des probabilités
        probabilities = pipeline_branch.predict_proba(df_input)[0]
        classes_noms = label_encoder_branch.classes_
        
        top3_indices = np.argsort(probabilities)[::-1][:3]

        recommandations = []
        for rank, idx in enumerate(top3_indices, 1):
            recommandations.append({
                "rang": rank,
                "branche": classes_noms[idx].replace("_", " ").title(),
                "probabilite": round(float(probabilities[idx]) * 100, 1)
            })

        return {"recommandations": recommandations}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la prédiction de branche : {str(e)}")