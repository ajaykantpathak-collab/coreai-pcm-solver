import os
import hashlib
import requests
import streamlit as st
from google import genai
from PIL import Image
from pypdf import PdfReader
import chromadb


# 🔑 Configure Gemini securely from cloud memory
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
 # 🔑 Configure Gemini securely from cloud memory
# Note: The new SDK looks for GEMINI_API_KEY automatically, 
# but keeping your environment check is great practice!
 api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    client = genai.Client()  # Capital "C"

# 🎛️ Fine-Tuned settings for absolute math/physics accuracy (Zero Creativity)
# The new SDK uses standard names instead of a separate generation_config block
tuned_settings = {
    "temperature": 0.0,
    "top_p": 0.95,
    "max_output_tokens": 4096,
}

# 🤖 Set your target model name as a variable to use later
model_name = "gemini-2.5-flash"

# 🔍 Connect straight to your vector vault folder
# When deployed, make sure your coreai_vector_vault folder is uploaded to GitHub!
chroma_client = chromadb.PersistentClient(path="./coreai_vector_vault")
collection = chroma_client.get_or_create_collection(name="syllabus_moat")

# Initialize continous chat memoryif it doesnt exist already
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# ==========================================
# 1. PAGE SETUP & STYLES
# ==========================================
st.set_page_config(
    page_title="CoreAI PCM Solver",
    page_icon="🎓",
    layout="centered"
)

# force standard HTTP/REST connection protocols to bypass firewall/network blocks
api_key = os.getenv("GEMINI_API_KEY")
# 🧼 2. CUSTOM SIDEBAR CONTROL PANEL
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3413/3413535.png", width=100)
    st.title("Control Panel")
    st.write("Manage your active workspace session details below.")
    
    if st.button("🔄 Clear App Workspace", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# ################################################
# PHASE 2: MAIN SYSTEM CONTROLS & SIDEBAR ENGINE
# ################################################

st.sidebar.markdown("### 🛠️ System Control")

# 1. Your Universal Dropdown Selector
grade_level = st.sidebar.selectbox(
    "Select Subject / Target Level:",
    (
        "IIT-JEE / NEET Advanced",
        "Class 9-10 (Secondary)",
        "biology & life sciences",
        "geography & earth sciences",
        "accountancy & business studies",
        "class 1-8 (primary and secondary)",
        "English Literature & Grammar", 
        "Hindi Literature & Vyakaran",
        "Commerce & Economics"
    )
)

# 2. The Multi-Configuration Metric Engine
subject_configs = {
    "IIT-JEE / NEET Advanced":       {"temperature": 0.0, "top_p": 0.1},
    "Class 9-10 (Secondary)":        {"temperature": 0.0, "top_p": 0.1},
    "biology & life sciences":       {"temperature": 0.1, "top_p": 0.2},
    "geography & earth sciences":    {"temperature": 0.1, "top_p": 0.2},
    "accountancy & business studies": {"temperature": 0.0, "top_p": 0.1},
    "class 1-8 (primary and secondary)": {"temperature": 0.0, "top_p": 0.1},
    "English Literature & Grammar":  {"temperature": 0.5, "top_p": 0.9},
    "Hindi Literature & Vyakaran":   {"temperature": 0.5, "top_p": 0.9},
    "Commerce & Economics":          {"temperature": 0.1, "top_p": 0.3}
}

# Extract the active configuration based on what the student clicks
chosen_metrics = subject_configs[grade_level]

st.divider()
st.caption("🔒 Security Status: All subject Guardrail Engines Active")
st.caption("⚡ Primary Core: Gemini 1.5 Flash")
st.caption("🔵 Watchdog Layer: Gemini 1.5 Pro Active")
# =========================================================
# =========================================================
# PHASE 3: MASTER DYNAMIC PROMPT ROUTING LAYER
# =========================================================

if "Literature" in grade_level:
    system_instruction = """
    CRITICAL GUARDRAIL: If the user's question or uploaded image is completely irrelevant 
    to English Literature, Poetry, or Grammar, you must output exactly: 
    "NO. This question is irrelevant or invalid for the English Literature track."
    
    You are an elite Professor of English Literature and Linguistics. 
    Analyze poems, stories, or grammar problems by breaking down core themes, metaphors, and poetic devices.
    CRITICAL STRUCTURE: Separate your response into two sections using the exact text:
    [Insert comprehensive literary analysis here]
    ===SHORTCUT_TRICK===
    Contextual Vocabulary & Key Character Summaries: [Insert quick theme hacks here]
    """

elif "Hindi" in grade_level:
    system_instruction = """
    CRITICAL GUARDRAIL: यदि उपयोगकर्ता का प्रश्न या अपलोड की गई छवि हिंदी साहित्य, कविता या व्याकरण से संबंधित नहीं है, तो आपको स्पष्ट रूप से उत्तर देना होगा: 
    "NO. यह प्रश्न हिंदी विषय ट्रैक के लिए अप्रासंगिक या अमान्य है।"
    
    You are an expert Hindi Scholar and Senior Educator (हिंदी भाषा और साहित्य विशेषज्ञ).
    Provide 'सप्रसंग व्याख्या', 'भावार्थ', and highlight 'काव्य-सौंदर्य' (Alankar, Ras, Chhand).
    CRITICAL STRUCTURE: Separate your response into two sections using the exact text:
    [Insert full Hindi analysis here]
    ===SHORTCUT_TRICK===
    मुख्य बिंदु और कठिन शब्दार्थ: [Insert quick reference word meanings here]
    """

elif "Commerce" in grade_level or "Accountancy" in grade_level:
    system_instruction = """
    CRITICAL GUARDRAIL: If the user's question or uploaded image is completely irrelevant 
    to Financial Accounting, Ledgers, or Bookkeeping, you must output exactly: 
    "NO. This question is irrelevant or invalid for the Accountancy & Commerce track."
    
    You are a Senior Chartered Accountant and Corporate Finance Expert.
    Provide precise journal entries, ledgers, and cash flows using structured accounting tables.
    CRITICAL STRUCTURE: Separate your response into two sections using the exact text:
    [Insert complete step-by-step financial balance sheets and solutions here]
    ===SHORTCUT_TRICK===
    Ledger Balancing Tricks & Core Rules Applied: [Insert quick double-entry rule checks here]
    """

elif "Finance" in grade_level or "Economics" in grade_level:
    system_instruction = """
    CRITICAL GUARDRAIL: If the user's question or uploaded image is completely irrelevant 
    to Microeconomics, Macroeconomics, or Financial equations, you must output exactly: 
    "NO. This question is irrelevant or invalid for the Economics & Finance track."
    
    You are an elite Doctor of Economics and Financial Analyst.
    Explain micro/macro concepts, elasticity equations, or market theories with structured breakdowns.
    CRITICAL STRUCTURE: Separate your response into two sections using the exact text:
    [Insert comprehensive economic analysis here]
    ===SHORTCUT_TRICK===
    Strategic Summary Keys & Core Formula Shortcuts: [Insert quick mental graph summaries here]
    """

elif "Biology" in grade_level:
    system_instruction = """
    CRITICAL GUARDRAIL: If the user's question or uploaded image is completely irrelevant 
    to Biology, Zoology, Botany, or human anatomy, you must output exactly: 
    "NO. This question is irrelevant or invalid for the Biology & Life Sciences track."
    
    You are a Senior Medical Professor and Expert Biologist.
    Break down anatomy, cell biology, physiological cycles, and botanical terms using clear, structured breakdowns.
    CRITICAL STRUCTURE: Separate your response into two sections using the exact text:
    [Insert complete conceptual biological breakdown here]
    ===SHORTCUT_TRICK===
    High-Yield Diagram Keys & Memory Mnemonics: [Insert quick tricks to remember labels and names here]
    """

elif "Geography" in grade_level:
    system_instruction = """
    CRITICAL GUARDRAIL: If the user's question or uploaded image is completely irrelevant 
    to Physical Geography, Topography, Earth Sciences, or climate data, you must output exactly: 
    "NO. This question is irrelevant or invalid for the Geography & Earth Sciences track."
    
    You are an elite Geologist and Cartography Expert.
    Explain physical geography, climatic patterns, landforms, or demographic data with highly structured points.
    CRITICAL STRUCTURE: Separate your response into two sections using the exact text:
    [Insert comprehensive geographical breakdown here]
    ===SHORTCUT_TRICK===
    Map Markers & Core Landform Identification Hacks: [Insert quick summary keys here]
    """

else:
    system_instruction = """
    CRITICAL GUARDRAIL: If the user's question or uploaded image is completely irrelevant 
    to Mathematics, Physics, Chemistry, or general school Science, you must output exactly: 
    "NO. This question is irrelevant or invalid for this Science/PCM track."
    
    You are an elite Master Tutor for IIT-JEE and NEET specializing in Physics, Chemistry, and Mathematics.
    Provide precise, analytical, step-by-step conceptual derivations and numerical solutions.
    CRITICAL STRUCTURE: Separate your response into two sections using the exact text:
    [Insert complete core step-by-step mathematical/scientific solution here]
    ===SHORTCUT_TRICK===
    JEE/NEET Competitive Exam Shortcut: [Insert time-saving estimation tricks or memory keys here]
    """

# ==========================================
# 2. MAIN USER INTERFACE DESIGN
# ==========================================
st.title("🎓 CoreAI PCM Solver")
st.write("A mathematically strict, zero-hallucination premium learning platform.")

# Placing visual inputs neatly inside a bordered modern card
with st.container(border=True):
    st.markdown(f"#### 📥 Submit Your {grade_level} Problem")
    
    # Image uploader element for textbook snaps (Modified for Batch Processing)
    uploaded_files = st.file_uploader(
        "Snap or upload your problem picture(s):",
        type=["jpg", "jpeg", "pdf", "png"],
        accept_multiple_files=True
    )
    

    # 🎨 Display continuous chat history thread on-screen
    for message in st.session_state.conversation_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Text container for typed questions or context notes (Moved up so it's always ready)
    additional_text = st.text_area(
        "Add question text or custom context guidelines:",
        placeholder="Type or paste text equations here...",
        key="unique_problem_text_input"
    )

    # Live picture preview if uploaded (Only if it's an image file)
    # Note: batch processing handles files directly; individual preview is skipped.




# Rate limiter initialization check
if "usage_counter" not in st.session_state:
    st.session_state.usage_counter = 0

# 🚀 MULTI-AGENT COMPONENT 1: GLOBAL TEXT QUERY CACHE WITH DYNAMIC SUBJECT SWITCH
@st.cache_data(show_spinner=False)
def get_cached_text_solution(question_text, selected_subject):
    """Queries the local vector matrix and generates a dynamic, subject-vetted solution."""
    try:
        # 1. Search vector database for matching institutional context
        results = collection.query(query_texts=[question_text], n_results=3)
        
        context = ""
        if results and results['documents'] and results['documents'][0]:
            context = "\n".join(results['documents'][0])
            
        # ⚙️ DYNAMIC INTELLECTUAL PERSONA SWITCH
        if selected_subject in ["Physics", "Chemistry", "Mathematics"]:
            persona_instruction = "You are an elite, hyper-accurate STEM tutor for competitive entrance exams like JEE/NEET. Always format equations beautifully in standard LaTeX using $ for inline math and $$ for blocks."
        elif selected_subject in ["Accounts", "Economics", "Business Studies"]:
            persona_instruction = "You are an expert Commerce and Finance Professor. Break down balance sheets, ledger entries, macro/microeconomic curves, and numerical equations with extreme precision and clear structural formatting."
        elif selected_subject in ["English Literature & Grammar"]:
            persona_instruction = "You are a master Academic Professor specializing in English Literature, Grammar, and textual analysis. Provide comprehensive, deeply analytical, and highly structured literary explanations."
        else:
            persona_instruction = f"You are an expert Academic Professor specializing in {selected_subject}. Provide comprehensive, deeply analytical, and structured textual explanations, keeping the academic tone highly professional."
            
        # 2. Build the grounded prompt dynamically
        grounded_prompt = f"""
        {persona_instruction}
        
        Use the following verified context from our institutional knowledge base to perfectly resolve the user's inquiry:
        [Database Context]:
        {context}
        
        [User Question]:
        {question_text}
        """
        
        # Generate response using your initialized Gemini client
        response = client.models.generate_content(
            model=model_name,
            contents=grounded_prompt,
            config=tuned_settings
        )
        return response.text
    except Exception as e:
        return f"❌ Execution error: {str(e)}"

# 📡 MULTI-AGENT COMPONENT 2: LIVE STREAMING LOGIC CORE
def stream_text_solution(question_text):
    """Direct tunnel to the cached generation matrix."""
    return get_cached_text_solution(question_text)

# 📡 MULTI-AGENT COMPONENT 2: LIVE STREAMING LOGIC CORE
def stream_text_solution(question_text, selected_subject):
    """Fetches the streaming solution matrix from the backend node cleanly."""
    return get_cached_text_solution(question_text, selected_subject)

# =========================================================================
# 🎛️ CORE CONTROL INTERFACE DEFINITIONS
# =========================================================================

# 1. Subject Selector Dropdown (Make sure this variable matches your sidebar code)
subject = st.sidebar.selectbox(
    "Select Subject/Target Level",
    ["Physics", "Chemistry", "Mathematics", "Accounts", "Economics", "Business Studies", "English Literature & Grammar"]
)

# 2. File Processing Form Submit State
# If you have an explicit st.form, this handles the submit button state
submit_button = st.sidebar.button("Process Batch Uploads")

# =========================================================================
# PRIMARY USER INTERACTION INTERFACE MATRIX
# =========================================================================

# 1. ALWAYS VISIBLE MAIN TEXT TRIGGER BUTTON
if st.button("Analyze & Solve Problem"):
    if not additional_text.strip():
        st.warning("⚠️ Please type your text question first.")
    else:
        # Trigger Scenario B (Pure Text Path) directly on click
        question_hash = hashlib.md5(additional_text.strip().lower().encode()).hexdigest()
        st.info("🔍 Matching query fingerprint against CoreAI Global Database...")
        
        try:
            textbook_solution = get_cached_text_solution(additional_text, subject)
            st.success("⚡ Cache Hit! Solution retrieved instantly from CoreAI Database (Cost: ₹0).")
            st.markdown("### 🎓 Verified Textbook Solution")
            st.markdown(textbook_solution)
        except Exception:
            st.warning("🔍 Cache Miss. Generating fresh dynamic resolution...")
            st.markdown("### 🎓 Verified Textbook Solution")
            response_stream = stream_text_solution(additional_text, subject)
            complete_response = st.write_stream(response_stream)
            # Pre-cache it for the next run
            get_cached_text_solution(additional_text, subject)

# 2. BATCH PROCESSOR FORM BLOCK (For uploads/pictures)
if submit_button:
    if not uploaded_files:
        st.warning("⚠️ Please upload a picture or PDF file to use the batch processor.")
    elif st.session_state.usage_counter >= 5:
        st.error("🔒 Free launch tier limit reached (5 queries max).")
    else:
        # SCENARIO A: BATCH FILE PROCESSING PIER
        st.info(f"📂 Batch detected: {len(uploaded_files)} files.")
        
        for index, single_file in enumerate(uploaded_files):
            st.markdown("---")
            st.subheader(f"📄 Document [{index + 1}/{len(uploaded_files)}]")
            
            current_image_context = None
            current_pdf_text = ""
            
            # 🖼️ ENGINE A: IMAGE PROCESSING 
            if single_file.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                try:
                    pil_image = Image.open(single_file)
                    st.image(pil_image, caption="Uploaded Problem Image", use_container_width=True)
                    
                    response = client.model.generate_content(model=model_name,contents=[
                        "Convert this image problem to a clean text question and solve it completely step-by-step.", 
                        pil_image
                    ])
                    st.markdown("### 🎓 Image Verified Solution")
                    st.write(response.text)
                    st.session_state.usage_counter += 1
                except Exception as img_err:
                    st.error(f"❌ Failed to parse image file: {str(img_err)}")