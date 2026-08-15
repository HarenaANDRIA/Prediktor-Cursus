from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import joblib
import pandas as pd
import numpy as np
import os

app = FastAPI(title="API Orientation ML")

# Autoriser l'application React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chargement des artefacts depuis le dossier models
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pipeline_path = os.path.join(BASE_DIR, "models", "best_pipeline_filiere.joblib")
encoder_path = os.path.join(BASE_DIR, "models", "label_encoder.joblib")

pipeline = joblib.load(pipeline_path)
label_encoder = joblib.load(encoder_path)

class NotesEtudiant(BaseModel):
    mathematiques: float = Field(..., ge=0, le=20)
    physique_et_chimie: float = Field(..., ge=0, le=20)
    science_de_la_vie_et_de_la_terre: float = Field(..., ge=0, le=20)
    francais: float = Field(..., ge=0, le=20)
    anglais: float = Field(..., ge=0, le=20)
    philosophie: float = Field(..., ge=0, le=20)
    histoire_et_geographie: float = Field(..., ge=0, le=20)
    test_psychotechnique: float = Field(..., ge=0, le=20)

@app.post("/predict")
def predict(notes: NotesEtudiant):
    df_input = pd.DataFrame([notes.dict()])
    expected_cols = pipeline.feature_names_in_
    df_input = df_input[expected_cols]

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