import os
import sqlite3
import pandas as pd
import streamlit as pd_stream  # Using standard text formatting aliases
import streamlit as st
import google.generativeai as genai

# =====================================================================
# 1. INITIALIZE SQL DATABASE & LOAD YOUR 100,000 ROWS
# =====================================================================
DB_FILE = "superapp_vault.db"
conn = sqlite3.connect(DB_FILE, check_same_thread=False)
cursor = conn.cursor()

# Create a clean SQL table architecture
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

# Automatically migrate your local CSV files into SQL if the DB is empty
cursor.execute("SELECT COUNT(*) FROM academic_vault")
if cursor.fetchone()[0] == 0:
    st.info("📦 Migrating 100,000 rows into local SQL Database... Please wait seconds.")
    csv_paths = [
        "./SuperApp_Data_Vault/K12/ncert_master.csv",
        "./SuperApp_Data_Vault/Competitive/jee_neet_30yr_master.csv",
        "./SuperApp_Data_Vault/Professional/ca_cs_accounts_master.csv"
    ]
    for path in csv_paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            # Match standard SQL columns
            if 'Class' not in df.columns: df['Class'] = "All"
            if 'Subject' not in df.columns: df['Subject'] = "General"
            
            df = df[['Class', 'Subject', 'Question', 'Detailed_Solution', 'stream_domain']]
            df.to_sql("academic_vault", conn, if_exists="append", index=False)
    conn.commit()

# =====================================================================
# 2. CONFIGURING THE GOOGLE AI CORE ENGINE
# =====================================================================
# Setup your API key securely
GOOGLE_API_KEY = "AIzaSyAio0usO4HWW73etoGcAs-1NZ7Ks9sY-MA" 
genai.configure(api_key=GOOGLE_API_KEY)

# =====================================================================
# 3. STREAMLIT FRONTEND USER INTERFACE
# =====================================================================
st.set_page_config(page_title="SuperApp Intelligence Hub", layout="wide")
st.title("🦅 SuperApp Production Intelligence Core")
st.caption("Enterprise-grade database search engine powered by SQL & Gemini Flash")

# Sidebar navigation filters
st.sidebar.header("🎯 Target Stream Filter")
stream_choice = st.sidebar.selectbox("Select Academic Domain", ["K12_CBSE", "COMP_JEE", "COMP_NEET", "PROF_CA_CS"])

# Main input search query bar
user_query = st.text_input("💬 Ask your academic context or specific exam question:")

if user_query:
    st.write("---")
    
    # STEP A: High-Speed SQL Database Scan (Bypasses token limits completely)
    # Searches keywords from user query inside the matched domain stream
    search_term = f"%{user_query.split()[0]}%" if len(user_query.split()) > 0 else "%"
    
    cursor.execute("""
        SELECT question, detailed_solution FROM academic_vault 
        WHERE stream_domain = ? AND question LIKE ? LIMIT 1
    """, (stream_choice, search_term))
    
    db_match = cursor.fetchone()
    
    # STEP B: Construct Context Grounding
    if db_match:
        context_data = f"Database Question: {db_match[0]}\nDatabase Verified Solution: {db_match[1]}"
        status_msg = "🎯 Grounded Row Located inside SQL Vault"
    else:
        context_data = "No explicit table row match found. Utilize general textbook physics/math parameters."
        status_msg = "🔍 Indice Scan Active (Standard Derivation Mode)"
        
    st.sidebar.success(status_msg)

    # STEP C: Execute Token-Optimized AI Context Query
    system_instruction = """
    You are an expert Indian EdTech educator. Use the provided database context to answer the student's question perfectly.
    You must format your response with explicit bold headers:
    - 🎯 Core Concept Breakdown
    - 🧮 Step-by-Step Derivation / Statutory Analysis
    - 💡 Concrete Real-World Example (Include simple day-to-day visualization elements)
    """
    
    prompt = f"Database Context:\n{context_data}\n\nStudent Question: {user_query}"
    
    with st.spinner("🧠 Scanning data vectors and formatting response..."):
        model = genai.GenerativeModel(
            model_name="gemini-3-flash-preview", # Running optimized Flash tier
            generation_config={"temperature": 0.0} # Absolute calculation lock
        )
        response = model.generate_content([system_instruction, prompt])
        
        # Output clean response to screen
        st.markdown(response.text)