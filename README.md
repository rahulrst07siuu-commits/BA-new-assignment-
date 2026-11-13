# SIP Shield Direction Predictor

A simple Streamlit app that estimates whether the next monthly Nifty 50 return may be positive or non-positive.

## Important compatibility note

The included model was serialized with **scikit-learn 1.8.0**. Install the exact version listed in `requirements.txt`. Using an older or different scikit-learn version can cause errors such as `No module named '_loss'` when loading the model.

## Run locally

1. Keep `app.py`, `sip_shield_direction_model.joblib`, and `requirements.txt` in the same folder.
2. Open a terminal in that folder.
3. (Recommended) Create and activate a fresh virtual environment.
4. Install dependencies:

   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. Start the app:

   ```bash
   streamlit run app.py
   ```

If you previously installed another scikit-learn version in the same environment, run `pip install --force-reinstall scikit-learn==1.8.0` and restart the app. A fresh virtual environment is safer.

## Files

- `app.py` — Streamlit interface
- `sip_shield_direction_model.joblib` — trained prediction model and input defaults
- `model_comparison.xlsx` — model comparison results
- `requirements.txt` — dependencies with the required scikit-learn version

## Notes

This is an experimental model based on a limited historical sample. Its output is not a guaranteed forecast or investment recommendation. Some engineered/calendar features are held at their historical default values by the app.
