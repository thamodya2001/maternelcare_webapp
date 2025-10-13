# streamlit_app.py
import streamlit as st
from PIL import Image

# --- PAGE SETUP ---
home_page = st.Page(
    "views/home.py",
    title="Home",
    icon=":material/home:",
    default=True,
)
predict_page = st.Page(
    "views/predict.py",
    title="Predict Risk",
    icon=":material/warning:"
)


contact_page = st.Page(
    "forms/contact.py",
    title="Contact & Feedback",
    icon=":material/contact_mail:",
)

# --- NAVIGATION SETUP ---
pg = st.navigation(
    {
        "🌸 MaternelCare AI": [home_page,predict_page],
        "📨 Support": [contact_page],
    }
)
st.sidebar.markdown("""
---
### 🤰 MaternelCare AI
Empowering mothers with intelligent health predictions.  
Navigate through the sections to explore tools and insights designed for better maternal well-being.

Made with ❤️ by **Team MaternelCare**
""")

# --- PAGE RUNNER ---
pg.run()
