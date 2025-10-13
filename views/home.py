import streamlit as st
from PIL import Image

# ---- PAGE SETTINGS ----
st.set_page_config(page_title="MaternelCare AI", page_icon="🤰", layout="wide")

# ---- CUSTOM CSS FOR DUAL THEME SUPPORT ----
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap');

    /* General styles for both light and dark themes */
    .main-title {
        font-family: 'Playfair Display', serif;
        font-size: 70px;
        text-align: center;
        font-weight: 700;
        letter-spacing: 2px;
        margin-top: 20px;
    }
    .subtitle {
        text-align: center;
        font-size: 25px;
        font-style: italic;
        margin-bottom: 40px;
    }
    .stButton>button {
        background-color: #e91e63;
        color: white;
        border-radius: 15px;
        font-size: 18px;
        height: 3em;
        width: 15em;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #d81b60;
        transform: scale(1.05);
    }
    .feature-card {
        border-radius: 1.5em;
        box-shadow: 0 0.25em 1em rgba(0,0,0,0.1);
        padding: 1.5em;
        text-align: center;
        margin: 0.5em;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .feature-icon {
        font-size: 50px;
    }
    .feature-title {
        font-weight: bold;
        font-size: 18px;
    }
    .feature-desc {
        font-size: 15px;
    }
    
    /* Styles specifically for the light theme */
    [data-theme="light"] .main-title {
        color: #e91e63;
        text-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    [data-theme="light"] .subtitle {
        color: #666;
    }
    [data-theme="light"] .feature-card {
        background-color: white;
    }
    [data-theme="light"] .feature-title {
        color: #c2185b;
    }
    [data-theme="light"] .feature-desc {
        color: #555;
    }

    /* Styles specifically for the dark theme */
    [data-theme="dark"] .main-title {
        color: #ff91b8; /* Lighter pink for dark background */
        text-shadow: none;
    }
    [data-theme="dark"] .subtitle {
        color: #ccc;
    }
    [data-theme="dark"] .feature-card {
        background-color: #2b2b2b; /* A dark gray for the cards */
    }
    [data-theme="dark"] .feature-title {
        color: #ff91b8;
    }
    [data-theme="dark"] .feature-desc {
        color: #bbb;
    }

</style>
""", unsafe_allow_html=True)

# ---- HEADER SECTION ----
st.markdown("<h1 class='main-title'>MaternelCare AI 🤰</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Empowering Mothers with Intelligent Health Predictions</p>", unsafe_allow_html=True)

# ---- INTRO SECTION ----
col1, col2 = st.columns([1, 1.5])

with col1:
    try:
        image = Image.open("assets/pic2.jpg")
        st.image(image, caption="Healthy Mother, Healthy Future", use_container_width=True)
    except FileNotFoundError:
        st.warning("Image 'assets/pic2.jpg' not found. Please ensure the file exists in the 'assets' folder.")

with col2:
    st.markdown("""
    ### 🌼 Welcome to MaternelCare AI
    **MaternelCare AI** is an advanced platform that leverages **machine learning**
    to predict maternal health conditions and provide insights that support early intervention.

    Our platform uses **artificial intelligence** and **data-driven insights** to predict potential maternal health risks early — enabling doctors, families, and expectant mothers to take preventive action before complications arise.

    By combining **medical expertise** with **machine learning technology**, MaternelCare AI analyzes key health indicators such as **blood pressure**, **glucose levels**, **BMI**, and **medical history** to assess the risk level of each pregnancy.

    Our goal is simple: to support healthcare professionals and expecting mothers with **accurate, accessible**, and **proactive maternal risk assessment** — anytime, anywhere.
    """)

# ---- KEY FEATURES SECTION ----
st.markdown("<h1 style='text-align:center; color: #c2185b; margin-top:60px;'>Key Features</h1>", unsafe_allow_html=True)
colA, colB, colC = st.columns(3)

with colA:
    st.markdown("""
    <div class='feature-card'>
        <div class='feature-icon'>🧠</div>
        <div class='feature-title'>Predict Risk Levels</div>
        <p class='feature-desc'>AI-powered prediction of maternal health risk based on vital signs and medical history.</p>
    </div>
    """, unsafe_allow_html=True)

with colB:
    st.markdown("""
    <div class='feature-card'>
        <div class='feature-icon'>📊</div>
        <div class='feature-title'>Interactive Dashboards</div>
        <p class='feature-desc'>Visualize health data and track progress through intuitive, real-time dashboards.</p>
    </div>
    """, unsafe_allow_html=True)


with colC:
    st.markdown("""
    <div class='feature-card'>
        <div class='feature-icon'>🧍‍♀️</div>
        <div class='feature-title'>For Everyone</div>
        <p class='feature-desc'>Designed for both healthcare professionals and expectant mothers.</p>
    </div>
    """, unsafe_allow_html=True)

# ---- FOOTER ----
st.markdown("""
<hr>
<p style='text-align: center; color: gray;'>
Developed with ❤️ by Team MaternelCare | Powered by AI & Streamlit
</p>
""", unsafe_allow_html=True)