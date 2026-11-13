import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="SIP Shield Predictor", page_icon="📈", layout="wide")

st.markdown("""
<style>
.stButton > button {
    background-color: #C93649;
    color: white;
    border-radius: 8px;
    min-height: 44px;
    border: none;
    font-weight: 600;
}
.stButton > button:hover { background-color: #A92739; color: white; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_package():
    return joblib.load("sip_shield_direction_model.joblib")

try:
    package = load_package()
    model = package["model"]
    features = package["features"]
    defaults = package["feature_defaults"]
except Exception as e:
    st.error("Model file not found or could not be loaded. Keep "
             "'sip_shield_direction_model.joblib' in the same folder as app.py. "
             f"Details: {e}")
    st.stop()

st.title("📈 SIP Shield Predictor")
st.caption("Domestic SIP Shield Effect · Nifty 50 market direction")
st.write("Enter recent monthly market information to estimate whether the next monthly Nifty 50 return may be positive or non-positive.")

st.subheader("Market information")
c1, c2, c3 = st.columns(3)

with c1:
    sip = st.number_input("Previous month's SIP inflow (₹ crore)", min_value=0.0,
                          value=max(0.0, defaults["SIP_Lag1_cr"]), step=500.0)
    fii = st.number_input("Previous month's FII net flow (₹ crore)",
                          value=defaults["FII_Net_Flow_Lag1_cr"], step=1000.0)
    dii = st.number_input("Previous month's DII net flow (₹ crore)",
                          value=defaults["DII_Net_Flow_Lag1_cr"], step=1000.0)

with c2:
    sip_growth = st.number_input("Previous month's SIP growth (%)",
                                 value=defaults["SIP_Growth_Lag1_pct"], step=1.0)
    ret1 = st.number_input("Nifty return last month (%)",
                           value=defaults["Nifty_Return_Lag1_pct"], step=0.1)
    ret2 = st.number_input("Nifty return 2 months ago (%)",
                           value=defaults["Nifty_Return_Lag2_pct"], step=0.1)

with c3:
    ret3 = st.number_input("Nifty return 3 months ago (%)",
                           value=defaults["Nifty_Return_Lag3_pct"], step=0.1)
    vol3 = st.number_input("Previous 3-month volatility (%)",
                           min_value=0.0, value=max(0.0, defaults["Nifty_Volatility_3M_prior_pct"]), step=0.1)
    vol6 = st.number_input("Previous 6-month volatility (%)",
                           min_value=0.0, value=max(0.0, defaults["Nifty_Volatility_6M_prior_pct"]), step=0.1)

momentum3 = st.number_input("Previous 3-month Nifty momentum (%)",
                            value=defaults["Nifty_Momentum_3M_prior_pct"], step=0.1)
momentum6 = st.number_input("Previous 6-month Nifty momentum (%)",
                            value=defaults["Nifty_Momentum_6M_prior_pct"], step=0.1)
vol12 = st.number_input("Previous 12-month volatility (%)",
                        min_value=0.0, value=max(0.0, defaults["Nifty_Volatility_12M_prior_pct"]), step=0.1)

st.caption("Calendar seasonality inputs are held at historical median values. All entered figures should use the same units as the historical dataset.")

if st.button("Predict Market Direction"):
    fii_selling = 1 if fii < 0 else 0
    values = defaults.copy()
    values.update({
        "SIP_Lag1_cr": sip,
        "FII_Net_Flow_Lag1_cr": fii,
        "DII_Net_Flow_Lag1_cr": dii,
        "FII_Selling_Lag1": fii_selling,
        "SIP_Growth_Lag1_pct": sip_growth,
        "Nifty_Return_Lag1_pct": ret1,
        "Nifty_Return_Lag2_pct": ret2,
        "Nifty_Return_Lag3_pct": ret3,
        "Nifty_Momentum_3M_prior_pct": momentum3,
        "Nifty_Momentum_6M_prior_pct": momentum6,
        "Nifty_Volatility_3M_prior_pct": vol3,
        "Nifty_Volatility_6M_prior_pct": vol6,
        "Nifty_Volatility_12M_prior_pct": vol12,
        "FII_Selling_x_SIP_Lag1": fii_selling * (sip / 1000)
    })
    row = pd.DataFrame([[values[f] for f in features]], columns=features)
    prediction = int(model.predict(row)[0])
    st.divider()
    st.subheader("Prediction result")
    if prediction == 1:
        st.success("Estimated market direction: UP")
    else:
        st.warning("Estimated market direction: DOWN / NON-POSITIVE")
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(row)[0]
        classes = list(model.classes_)
        probs = dict(zip(classes, probabilities))
        st.write(f"Estimated UP probability: {probs.get(1, 0):.1%}")
        st.write(f"Estimated DOWN / NON-POSITIVE probability: {probs.get(0, 0):.1%}")
    st.caption("This is an experimental historical-model estimate, not a guaranteed market forecast or investment recommendation.")

with st.expander("About the model"):
    st.write(f"Selected model: {package['model_name']}")
    st.write(f"Historical observations used: {package['n_observations']}")
    st.write(f"Data period: {package['data_start']} to {package['data_end']}")
    st.write("The model is included in this application. No Excel upload is required.")
