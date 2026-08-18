import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, f1_score
from xgboost import XGBClassifier

os.makedirs('models', exist_ok=True)

def entrainer_et_evaluer_filiere(data_path, model_output_name, encoder_output_name, report_prefix):
    print("=" * 70)
    print(f"🚀 ENTRAÎNEMENT & SÉLECTION DE MODÈLE (FILIÈRE) : {data_path}")
    print("=" * 70)

    if not os.path.exists(data_path):
        print(f"⚠️ Fichier introuvable : {data_path}")
        return

    df = pd.read_csv(data_path, sep=';', decimal=',')
    target_col = 'filiere_recommandee'
    feature_cols = [col for col in df.columns if col != target_col]

    for col in feature_cols:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.'), errors='coerce')

    X = df[feature_cols]
    y_raw = df[target_col]

    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y_raw)

    joblib.dump(label_encoder, f'models/{encoder_output_name}')

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    candidates = {
        "XGBoost": {
            "pipeline": Pipeline([
                ('scaler', StandardScaler()),
                ('classifier', XGBClassifier(random_state=42, eval_metric='mlogloss'))
            ]),
            "param_grid": {
                'classifier__n_estimators': [100, 150],
                'classifier__max_depth': [4, 6],
                'classifier__learning_rate': [0.05, 0.1],
            },
        },
        "RandomForest": {
            "pipeline": Pipeline([
                ('scaler', StandardScaler()),
                ('classifier', RandomForestClassifier(random_state=42))
            ]),
            "param_grid": {
                'classifier__n_estimators': [150, 250],
                'classifier__max_depth': [None, 10],
            },
        },
    }

    results = {}
    for name, cfg in candidates.items():
        print(f"\n🔎 Recherche d'hyperparamètres pour {name}...")
        grid_search = GridSearchCV(
            estimator=cfg["pipeline"],
            param_grid=cfg["param_grid"],
            cv=cv,
            scoring='f1_macro',
            n_jobs=-1
        )
        grid_search.fit(X_train, y_train)
        results[name] = grid_search

    best_model_name = max(results, key=lambda name: results[name].best_score_)
    best_grid_search = results[best_model_name]
    best_pipeline = best_grid_search.best_estimator_

    print(f"\n🏆 Modèle retenu : {best_model_name} (F1 macro CV = {best_grid_search.best_score_ * 100:.2f}%)")

    y_pred = best_pipeline.predict(X_test)
    test_f1 = f1_score(y_test, y_pred, average='macro')
    print(f"🎯 F1-Score Macro Test : {test_f1 * 100:.2f}%")

    joblib.dump(best_pipeline, f'models/{model_output_name}')
    with open(f'models/{report_prefix}_model_report.txt', 'w', encoding='utf-8') as f:
        f.write(f"Dataset : {data_path}\nModèle retenu : {best_model_name}\n")
        f.write(f"F1-Score macro (CV) : {best_grid_search.best_score_ * 100:.2f}%\n")
        f.write(f"F1-Score macro (Test) : {test_f1 * 100:.2f}%\n\n")
        f.write(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

    print(f"✅ Pipeline sauvegardé dans 'models/{model_output_name}'.\n")

def entrainer_et_evaluer_branche(data_path, model_output_name, encoder_output_name, report_prefix):
    print("=" * 70)
    print(f"🚀 ENTRAÎNEMENT & SÉLECTION DE MODÈLE (BRANCHE) : {data_path}")
    print("=" * 70)

    if not os.path.exists(data_path):
        print(f"⚠️ Fichier introuvable : {data_path}")
        return

    df = pd.read_csv(data_path, sep=';', decimal=',')
    target_col = 'branche_recommandee'

    X_raw = df.drop(columns=[target_col])
    y_raw = df[target_col]

    X = pd.get_dummies(X_raw, columns=['filiere'], drop_first=False)
    for col in X.columns:
        X[col] = pd.to_numeric(X[col], errors='coerce').astype(float)

    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y_raw)

    joblib.dump(label_encoder, f'models/{encoder_output_name}')

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    candidates = {
        "XGBoost": {
            "pipeline": Pipeline([
                ('scaler', StandardScaler()),
                ('classifier', XGBClassifier(random_state=42, eval_metric='mlogloss'))
            ]),
            "param_grid": {
                'classifier__n_estimators': [100, 150],
                'classifier__max_depth': [4, 6],
            },
        },
    }

    results = {}
    for name, cfg in candidates.items():
        grid_search = GridSearchCV(
            estimator=cfg["pipeline"],
            param_grid=cfg["param_grid"],
            cv=cv,
            scoring='f1_macro',
            n_jobs=-1
        )
        grid_search.fit(X_train, y_train)
        results[name] = grid_search

    best_model_name = max(results, key=lambda name: results[name].best_score_)
    best_grid_search = results[best_model_name]
    best_pipeline = best_grid_search.best_estimator_

    joblib.dump(best_pipeline, f'models/{model_output_name}')
    print(f"✅ Pipeline Branche sauvegardé dans 'models/{model_output_name}'.\n")

if __name__ == '__main__':
    series_list = ['aucune', 'scientifique', 'litteraire', 'ose']

    for serie in series_list:
        entrainer_et_evaluer_filiere(
            data_path=f'data/processed/cleaned_bac_{serie}.csv',
            model_output_name=f'best_pipeline_filiere_{serie}.joblib',
            encoder_output_name=f'label_encoder_filiere_{serie}.joblib',
            report_prefix=f'filiere_{serie}'
        )

    entrainer_et_evaluer_branche(
        data_path='data/processed/dataset_branch_cleaned.csv',
        model_output_name='best_pipeline_branch.joblib',
        encoder_output_name='label_encoder_branch.joblib',
        report_prefix='branch'
    )