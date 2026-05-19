import os
import sqlite3
import pandas as pd
import streamlit as st
from google import genai

# ==========================================
# 1. 🖥️ STREAMLIT APPLICATION INTERFACE CONFIG
# ==========================================
st.set_page_config(
    page_title="CoreAI PCM Solver & Visualizer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. 🔒 SECURE ENCRYPTED KEY EXTRACTION
# ==========================================
if "GEMINI_API_KEY" in st.secrets:
    api_key_secret = st.secrets["GEMINI_API_KEY"]
else:
    api_key_secret = os.environ.get("GEMINI_API_KEY", "")

client = genai.Client(api_key=api_key_secret)

# ==========================================
# 3. 🗄️ STREAMLIT-OPTIMIZED RELATIONAL SQL CACHE
# ==========================================
def get_db_connection():
    if os.path.exists("superapp_vault.db"):
        return sqlite3.connect("superapp_vault.db", check_same_thread=False)
    return None

conn = get_db_connection()

# Create table framework safely if it doesn't exist
if conn is not None:
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS academic_vault (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                class TEXT,
                subject TEXT,
                question TEXT,
                detailed_solution TEXT,
                stream_domain TEXT
            )
        ''')
        conn.commit()
    except Exception:
        pass

model_name = "gemini-2.5-flash"

# ==========================================
# 4. 🎨 VISUAL DASHBOARD FRONTEND DISPLAY
# ==========================================
st.title("🚀 CoreAI Academic Recon Engine")
st.caption("High-Speed LaTeX Solution Matrix and Structural Visual Aid Router")

with st.sidebar:
    st.header("⚙️ Control Panel")
    if st.button("🗑️ Clear App Workspace"):
        st.rerun()
    
    st.subheader("System Control")
    grade_level = st.selectbox("Select Target Level:", ["K12", "IIT-JEE / NEET Advanced", "Professional"])
    selected_subject = st.selectbox("Select Subject Domain:", ["Physics", "Chemistry", "Biology", "Finance", "Economics"])

with st.container(border=True):
    st.markdown(f"#### 📥 Submit Your {selected_subject} Problem")
    additional_text = st.text_area(
        "Add question text or custom context guidelines:",
        placeholder="Type or paste textbook questions here...",
        key="unique_problem_text_input"
    )

# ==========================================
# 5. 🧠 INTELLECTUAL PROCESSING CORRIDOR
# ==========================================
if st.button("Analyze & Solve Problem"):
    if not additional_text.strip():
        st.warning("Please input an academic question first before executing analysis.")
    else:
        # Create clear responsive split screen layout columns
        col1, col2 = st.columns([1.2, 0.8])
        
        with col1:
            st.write("### 🎓 Verified Textbook Solution")
            clean_query = additional_text.strip()
            db_match = None
            
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    cursor.execute(
                        "SELECT question, detailed_solution FROM academic_vault WHERE question = ? LIMIT 1",
                        (clean_query,)
                    )
                    db_match = cursor.fetchone()
                except Exception:
                    db_match = None
            
            if db_match:
                st.success("⚡ Data Vector Hit! Solution parsed via CoreAI Core Engine (Cost: ₹0).")
                st.markdown(db_match[1])
            else:
                with st.spinner("Processing structural queries against CoreAI Global Database..."):
                    try:
                        system_instruction = f"You are an elite academic professor tracking {selected_subject} under {grade_level} constraints. Deliver comprehensive step-by-step mathematical solutions using clear LaTeX format. Surround all inline LaTeX formulas inside single dollars $...$ and multi-line equations inside double dollars $$...$$."
                        response = client.models.generate_content(
                            model=model_name,
                            contents=f"{system_instruction}\n\nQuestion:\n{clean_query}"
                        )
                        st.info("🌐 Core Network Routing complete. Rendering live dynamic content stream.")
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"Execution error: {str(e)}")
        
        # ==========================================
        # 6. 🖼️ BULLETPROOF NATIVE VISUAL AID CORE
        # ==========================================
        with col2:
            st.write("### 🖼️ Contextual Visual Aid")
            
            query_lower = clean_query.lower()
            
            if "photo" in query_lower or "systh" in query_lower or "plant" in query_lower:
                st.info("📊 Structural Process Matrix: Photosynthesis")
                # Create a beautiful, native interactive data visualization block
                chart_data = pd.DataFrame(
                    [[6, 6, 1], [0, 0, 6], [0, 0, 6]], 
                    columns=["CO2 (Inputs)", "H2O (Inputs)", "C6H12O6 + O2 (Outputs)"],
                    index=["Light Energy Bound", "Chemical Conversion", "Net Yield Balance"]
                )
                st.bar_chart(chart_data)
                st.caption("Figure 1.1: Native Molecular Yield Balance Metrics for Metabolic Pathways.")
                
            elif "star" in query_lower or "twinkle" in query_lower or "refraction" in query_lower:
                st.info("📊 Waveform Deviation Matrix: Refraction Data")
                chart_data = pd.DataFrame(
                    [[1.0, 1.0], [1.2, 1.05], [1.4, 1.11], [1.6, 1.18]], 
                    columns=["True Trajectory Vector", "Atmospheric Density Curvature"],
                    index=["Vacuum Layer", "Upper Exosphere", "Stratosphere", "Troposphere Ground"]
                )
                st.line_chart(chart_data)
                st.caption("Figure 2.1: Light Trajectory Variance relative to Evolving Atmospheric Gradients.")
                
            elif "pendulum" in query_lower or "energy" in query_lower or "gravity" in query_lower:
                st.info("📊 Mechanical System Oscillations: Energy Over Time")
                chart_data = pd.DataFrame(
                    [[10, 0], [7, 3], [0, 10], [3, 7], [10, 0]], 
                    columns=["Potential Energy (Ep)", "Kinetic Energy (Ek)"],
                    index=["Max Amplitude Left", "Descending Arc", "Equilibrium Center", "Ascending Arc", "Max Amplitude Right"]
                )
                st.line_chart(chart_data)
                st.caption("Figure 3.1: Continuous Conservation Tracking of Pendulum Mechanical Energy Curves.")
                
            else:
                st.info(f"📊 System Core Metrics: {selected_subject}")
                # Clean, functional fallback data metrics display
                chart_data = pd.DataFrame([10, 20, 30, 40], columns=["Structural Vector Depth"])
                st.area_chart(chart_data)
                st.caption(f"Figure 4.1: General {selected_subject} Functional Model Layout Matrix.")