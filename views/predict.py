import streamlit as st
import pickle
import numpy as np
import pandas as pd

# ---- IMPORTANT: DEFINE THE MODEL'S EXPECTED FEATURE ORDER ----
# The feature order MUST match the columns used during model training exactly.
# This order is confirmed from the 'model_pickle' content and the notebook:
TRAINING_FEATURES = [
    'Age', 
    'Systolic BP', 
    'Diastolic', 
    'BS', 
    'Body Temp', 
    'BMI', 
    'Previous Complications', 
    'Preexisting Diabetes', 
    'Gestational Diabetes', 
    'Mental Health',
    'Heart Rate' # Note: Heart Rate was placed last in the model's feature_names_in_ list.
]

# ---- MODEL ENCODING MAPPING (Confirmed from Notebook Cell 73) ----
# 0: High Risk
# 1: Low Risk
RISK_MAPPING = {
    0: "HIGH RISK",
    1: "LOW RISK"
}

# ---- GUIDANCE CONTENT ----
# --- NOTE: The guidance below has been updated to prompt navigation ---
HIGH_RISK_GUIDANCE = """
**Immediate Action Required:**
1.  **Contact Your Healthcare Provider NOW:** Do not delay. Call your doctor or hospital immediately to report this assessment.
2.  **Monitor Vitals:** Keep a close watch on your Blood Pressure, Heart Rate, and Body Temperature.
3.  **Avoid Stress:** Rest completely and monitor for any new symptoms like severe headache, blurred vision, or swelling.


"""

LOW_RISK_GUIDANCE = """
**Maintain Healthy Habits:**
1.  **Continue Routine Checkups:** This assessment suggests a low risk, but regular prenatal care is essential to catch any future changes.
2.  **Healthy Diet & Hydration:** Ensure adequate nutrition and maintain excellent hydration.
3.  **Stay Active:** Follow your provider's advice on light exercise and sufficient rest.
4.  **Watch for Changes:** Report any unusual symptoms (e.g., unexpected bleeding, persistent pain) to your doctor immediately.


"""

# Page config
# NOTE: Renamed this page 'Home' so it is visible in the sidebar.
st.set_page_config(page_title="Maternal Risk Predictor", page_icon="🤰", layout="centered")

# --- CUSTOM CSS FOR BUTTON ---
st.markdown("""
<style>
    /* Styling the Streamlit primary button */
    .stButton>button {
        background-color: #e91e63 !important; /* Nice Pink */
        color: white !important;
        border-radius: 10px;
        font-size: 18px;
        height: 3em;
        width: 100%;
        border: 1px solid #e91e63;
        transition: background-color 0.3s, transform 0.1s;
    }
    .stButton>button:hover {
        background-color: #d81b60 !important; /* Slightly darker pink on hover */
        border: 1px solid #d81b60;
        transform: scale(1.01);
    }
    .main-title {
        color: #e91e63;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)
# --- END CUSTOM CSS ---


# Title
st.markdown("<h1 class='main-title'>🤰 Maternal Health Risk Predictor</h1>", unsafe_allow_html=True)
st.write("Enter patient details to assess maternal health risk level")

# Load model
model = None
try:
    # Assuming the model is accessible at this relative path
    with open("model/model_pickle.pkl", "rb") as file: 
        model = pickle.load(file)
    #st.success("✅ Model loaded successfully.")
except FileNotFoundError:
    st.error("❌ Model file not found. Please ensure the path 'model/model_pickle.pkl' is correct.")
    st.stop()
except Exception as e:
    st.error(f"❌ Error loading model: {str(e)}")
    st.info("The model might be incompatible with the current Python/Streamlit environment.")
    st.stop()


# Input form
st.subheader("Patient Information")

# Dictionary to hold all input values
input_values = {}

# Create two columns for better layout
col1, col2 = st.columns(2)

with col1:
    input_values['Age'] = st.number_input("Age", min_value=10, max_value=80, value=25)
    input_values['Systolic BP'] = st.number_input("Systolic BP (mmHg)", min_value=90, max_value=200, value=120)
    input_values['Diastolic'] = st.number_input("Diastolic BP (mmHg)", min_value=60, max_value=350, value=80)
    input_values['BS'] = st.number_input("Blood Sugar (mmol/L)", min_value=3, max_value=20, value=6)
    input_values['Body Temp'] = st.number_input("Body Temperature (°F)", min_value=95.0, max_value=104.0, value=98.0, step=0.1) 

with col2:
    input_values['BMI'] = st.number_input("Body Mass Index (BMI)", min_value=1.0, max_value=50.0, value=22.0, step=0.1)
    input_values['Heart Rate'] = st.number_input("Heart Rate (bpm)", min_value=10, max_value=200, value=75)
    
    # Select boxes 
    previous_comp_str = st.selectbox("Previous Complications", ["No", "Yes"])
    diabetes_str = st.selectbox("Preexisting Diabetes", ["No", "Yes"])
    gestational_str = st.selectbox("Gestational Diabetes", ["No", "Yes"])
    mental_health_str = st.selectbox("Mental Health Diagnosis", ["No", "Yes"])

# Predict button
if st.button("Predict Risk Level"):
    # Convert Yes/No strings to 1.0/0.0
    input_values['Previous Complications'] = 1.0 if previous_comp_str == "Yes" else 0.0
    input_values['Preexisting Diabetes'] = 1.0 if diabetes_str == "Yes" else 0.0
    input_values['Gestational Diabetes'] = 1.0 if gestational_str == "Yes" else 0.0
    input_values['Mental Health'] = 1.0 if mental_health_str == "Yes" else 0.0
    
    # 1. Create a DataFrame and ensure feature order
    input_df = pd.DataFrame([input_values])
    try:
        input_data_ordered = input_df[TRAINING_FEATURES]
    except KeyError as e:
        st.error(f"❌ Feature Mismatch Error. Missing feature: {e}.")
        st.stop()
        
    # Predict
    try:
        # Get prediction (0 or 1)
        prediction_encoded = model.predict(input_data_ordered)[0]
        
        # --- Calculate Confidence/Probability ---
        predicted_proba_score = None
        try:
            # Get probability array
            prediction_proba = model.predict_proba(input_data_ordered)[0]
            # Determine the probability of the predicted class (index 0 or 1)
            predicted_proba_score = prediction_proba[int(prediction_encoded)] * 100
        except AttributeError:
            # Handle models that don't support predict_proba (like some SVC setups)
            st.warning("Could not calculate prediction confidence (model does not support predict_proba).")
        
        prediction_key = int(prediction_encoded)
        result_text = RISK_MAPPING.get(prediction_key, "UNKNOWN RISK")
        
        confidence_text = ""
        if predicted_proba_score is not None:
             confidence_text = f"Confidence: **{predicted_proba_score:.2f}%**"
        
        # Display result
        if result_text == "HIGH RISK":
            st.markdown(f"""
            <div style='padding: 20px; border-radius: 15px; text-align: center; margin: 20px 0; background-color: #ffebee; border: 3px solid #f44336;'>
                <h2 style='color: #d32f2f; font-weight: bold;'>🩸 HIGH RISK</h2>
                <p>{confidence_text}</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(HIGH_RISK_GUIDANCE)
        elif result_text == "LOW RISK": 
            st.markdown(f"""
            <div style='padding: 20px; border-radius: 15px; text-align: center; margin: 20px 0; background-color: #e8f5e8; border: 3px solid #4caf50;'>
                <h2 style='color: #2e7d32; font-weight: bold;'>🌸 LOW RISK</h2>
                <p>{confidence_text}</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(LOW_RISK_GUIDANCE)
        else: 
            st.markdown(f"""
            <div style='padding: 20px; border-radius: 15px; text-align: center; margin: 20px 0; background-color: #fff3e0; border: 3px solid #ff9800;'>
                <h2 style='color: #ef6c00;'>⚠️ {result_text} ({prediction_key})</h2>
                <p>Consult with a healthcare provider.</p>
            </div>
            """, unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"❌ Prediction processing error: {str(e)}")
        st.info("A fatal error occurred during the prediction process.")

# Footer (Keeping the existing footer)
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Developed for maternal healthcare | Powered by AI</p>", unsafe_allow_html=True)
