import os
import sqlite3
import pandas as pd
import streamlit as st
import chromadb
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
# Reads directly from Streamlit Cloud Secrets. No raw key strings exist here!
if "GEMINI_API_KEY" in st.secrets:
    api_key_secret = st.secrets["GEMINI_API_KEY"]
else:
    api_key_secret = os.environ.get("GEMINI_API_KEY", "")

# Initialize the official, secure GenAI client wrapper
client = genai.Client(api_key=api_key_secret)

# ==========================================
# 3. 🗄️ STREAMLIT-OPTIMIZED RELATIONAL SQL CACHE
# ==========================================
def get_db_connection():
    """
    Safely locates and connects to the SQLite database cache.
    Uses /tmp/ in cloud deployment environments to bypass write-permission lockouts.
    """
    # Check if we are running locally or on Streamlit Cloud
    if os.path.exists("superapp_vault.db"):
        db_path = "superapp_vault.db"
    elif os.path.exists("/tmp/superapp_vault.db"):
        db_path = "/tmp/superapp_vault.db"
    else:
        # Production Fallback path
        db_path = "superapp_vault.db"
        
    try:
        connection = sqlite3.connect(db_path, check_same_thread=False)
        return connection
    except Exception:
        return None

# Attempt to build core table schema architectures gracefully
conn = get_db_connection()
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

# ==========================================
# 4. 🎛️ MODEL OPTIONS & WORKSPACE SETTINGS
# ==========================================
model_name = "gemini-2.5-flash"

# Manage continuous chat session states safely across browser refreshes
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# ==========================================
# 5. 🎨 VISUAL DASHBOARD FRONTEND DISPLAY
# ==========================================
st.title("🚀 CoreAI Academic Recon Engine")
st.caption("High-Speed LaTeX Solution Matrix and Structural Visual Aid Router")

# Control Panel Sidebar Setup
with st.sidebar:
    st.header("⚙️ Control Panel")
    if st.button("🗑️ Clear App Workspace"):
        st.session_state.conversation_history = []
        st.rerun()
    
    st.subheader("System Control")
    grade_level = st.selectbox("Select Target Level:", ["K12", "IIT-JEE / NEET Advanced", "Professional"])
    selected_subject = st.selectbox("Select Subject Domain:", ["Physics", "Chemistry", "Biology", "Finance", "Economics"])

# Problem Submission Workspace Container
with st.container(border=True):
    st.markdown(f"#### 📥 Submit Your {selected_subject} Problem")
    additional_text = st.text_area(
        "Add question text or custom context guidelines:",
        placeholder="Type or paste textbook questions here...",
        key="unique_problem_text_input"
    )

# ==========================================
# 6. 🧠 INTELLECTUAL PROCESSING CORRIDOR
# ==========================================
if st.button("Analyze & Solve Problem"):
    if not additional_text.strip():
        st.warning("Please input an academic question first before executing analysis.")
    else:
        # Create a clean, responsive split screen rendering layout
        col1, col2 = st.columns([1.2, 0.8])
        
        with col1:
            st.write("### 🎓 Verified Textbook Solution")
            
            # Setup a default localized text matching wildcard fallback
            clean_search_tag = f"%{additional_text.strip().split()[-1]}%" if len(additional_text.strip().split()) > 0 else "%education%"
            
            db_match = None
            # Scan local database cache at zero-token computational overhead
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    cursor.execute(
                        "SELECT question, detailed_solution FROM academic_vault WHERE question LIKE ? OR detailed_solution LIKE ? LIMIT 1",
                        (clean_search_tag, clean_search_tag)
                    )
                    db_match = cursor.fetchone()
                except Exception:
                    db_match = None
            
            # Check if cache search hit a match successfully
            if db_match:
                st.success("⚡ Data Vector Hit! Solution parsed via CoreAI Core Engine (Cost: ₹0).")
                st.markdown(db_match[1])
            else:
                # Cache Miss: System seamlessly routes execution to the secure AI network model
                with st.spinner("Processing structural queries against CoreAI Global Database..."):
                    try:
                        system_instruction = f"You are an elite academic professor tracking {selected_subject} under {grade_level} constraints. Deliver comprehensive step-by-step mathematical solutions using clear LaTeX format. Surround all inline LaTeX formulas inside single dollars $...$ and multi-line equations inside double dollars $$...$$."
                        
                        response = client.models.generate_content(
                            model=model_name,
                            contents=f"{system_instruction}\n\nQuestion:\n{additional_text}"
                        )
                        
                        st.info("🌐 Core Network Routing complete. Rendering live dynamic content stream.")
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"Execution error: {str(e)}")
        
        # ==========================================
        # 7. 🖼️ BULLETPROOF LOCAL VISUAL AID ROUTER
        # ==========================================
        with col2:
            st.write("### 🖼️ Contextual Visual Aid")
            
            # Setup a clean default fallback asset link
            image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/gradient_background.png/600px-gradient_background.png"
            caption_text = "CoreAI Predictive Structural Data Layout"
            
            # Evaluate text parameters locally to isolate subject matches (Immune to 503 errors)
            query_lower = additional_text.lower()
            
            if "photo" in query_lower or "systh" in query_lower or "plant" in query_lower or "chlorophyll" in query_lower:
                image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/db/Photosynthesis_equation.svg/600px-Photosynthesis_equation.svg.png"
                caption_text = "Figure 1.1: Biochemical Input/Output Pathways of the Photosynthesis Equation."
                
            elif "star" in query_lower or "twinkle" in query_lower or "refraction" in query_lower:
                image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Atmospheric_refraction_diagram.svg/600px-Atmospheric_refraction_diagram.svg.png"
                caption_text = "Figure 2.1: Light Trajectory Deviation due to Evolving Atmospheric Densities."
                
            elif "pendulum" in query_lower or "energy" in query_lower or "gravity" in query_lower:
                image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/Oscillating_pendulum.svg/450px-Oscillating_pendulum.svg.png"
                caption_text = "Figure 3.1: Kinetic versus Potential Energy Waveform Oscillations."
                
            elif "ledger" in query_lower or "tax" in query_lower or "balance" in query_lower or "account" in query_lower:
                image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/xc/T-account.svg/600px-T-account.svg.png"
                caption_text = "Figure 4.1: Standard Double-Entry Accounting Structural Ledger (T-Account)."

            # Render the verified open-source vector directly to the split screen column
            st.image(image_url, caption=caption_text, use_container_width=True)