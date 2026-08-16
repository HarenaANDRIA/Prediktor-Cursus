import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, f1_score
from xgboost import XGBClassifier

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

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', XGBClassifier(random_state=42, eval_metric='mlogloss'))
])

param_grid = {
    'classifier__n_estimators': [100, 150],
    'classifier__max_depth': [4, 6],
    'classifier__learning_rate': [0.05, 0.1]
}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
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
print(f"🎯 F1-Score Macro Test : {f1_score(y_test, y_pred, average='macro') * 100:.2f}%")
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

joblib.dump(best_pipeline, 'models/best_pipeline_filiere.joblib')
print("✅ Pipeline réentraîné avec les 15 matières et 25 filières.")