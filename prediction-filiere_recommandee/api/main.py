import os
import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="API Orientation ML", version="2.0")

# Autoriser l'application React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chargement des artefacts ML depuis le dossier 'models'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pipeline_path = os.path.join(BASE_DIR, "models", "best_pipeline_filiere.joblib")
encoder_path = os.path.join(BASE_DIR, "models", "label_encoder.joblib")

try:
    pipeline = joblib.load(pipeline_path)
    label_encoder = joblib.load(encoder_path)
except Exception as e:
    raise RuntimeError(f"Erreur de chargement des modèles ML : {e}")

# Schéma Pydantic incluant l'ensemble des 12 matières
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
    dessin_technique: float = Field(..., ge=0, le=20)
    statistiques_et_probabilites: float = Field(..., ge=0, le=20)
    biologie_appliquee_et_biotechnologie: float = Field(..., ge=0, le=20)

@app.post("/predict")
def predict(notes: NotesEtudiant):
    try:
        # Pydantic V2 : model_dump() (si vous êtes sur Pydantic V1, utilisez .dict())
        data_dict = notes.model_dump() if hasattr(notes, "model_dump") else notes.dict()
        df_input = pd.DataFrame([data_dict])

        # Alignement sur l'ordre exact des features attendu par le pipeline
        if hasattr(pipeline, "feature_names_in_"):
            df_input = df_input[pipeline.feature_names_in_]

        # Calcul des probabilités de prédiction
        probabilities = pipeline.predict_proba(df_input)[0]
        classes_noms = label_encoder.classes_
        
        # Tri des 3 meilleures filières
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
        raise HTTPException(status_code=500, detail=f"Erreur lors de la prédiction : {str(e)}")