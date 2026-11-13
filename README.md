# SIP Shield Direction Predictor

This app predicts monthly Nifty direction (UP vs DOWN/NON-POSITIVE) using a pre-trained classification model. No Excel upload is required in the app.

## Included
- `app.py` — Streamlit interface
- `requirements.txt` — dependencies
- `sip_shield_direction_model.joblib` — pre-trained model
- `model_comparison.xlsx` — time-series CV comparison from development

## Run on Windows
1. Extract the ZIP.
2. Open the extracted folder in Command Prompt or VS Code.
3. Run `python -m pip install -r requirements.txt`
4. Run `python -m streamlit run app.py`
5. Open the local URL shown in the terminal (usually http://localhost:8501).

## Deploy
Upload `app.py`, `requirements.txt`, and `sip_shield_direction_model.joblib` to the root of a GitHub repository. Deploy `app.py` using Streamlit Community Cloud.

## Model details
- Selected model by time-series CV balanced accuracy: Gradient Boosting
- Historical complete observations: 116
- Data period: 2017-02 to 2026-09
- Holdout test accuracy: 0.417
- Holdout balanced accuracy: 0.500
- Holdout F1: 0.588

These figures are development diagnostics, not guaranteed future performance. The dataset is small and the app is a research demonstration, not investment advice.
