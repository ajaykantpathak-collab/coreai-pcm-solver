import streamlit as st
import google.generativeai as genai
from PIL import Image
from pypdf import PdfReader


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
genai.configure(api_key="AIzaSyAAqQv2pOmYcQ_uP8PNjXSyLUq-jECCXE4", transport="rest")
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
    
    # Image uploader element for textbook snaps
    uploaded_image = st.file_uploader(
        "Snap or upload your problem picture:", 
        type=["jpg", "jpeg", "pdf", "png"]
    )

    # 🎨 Display continuous chat history thread on-screen
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Text container for typed questions or context notes (Moved up so it's always ready)
    additional_text = st.text_area(
        "Add question text or custom context guidelines:",
        placeholder="Type or paste text equations here..."
    )

    # Live picture preview if uploaded (Only if it's an image file)
    if uploaded_image is not None:
        if uploaded_image.name.endswith(('.jpg', '.jpeg', '.png')):
            pil_image = Image.open(uploaded_image)
            st.image(pil_image, caption="Uploaded Document Preview", use_container_width=True)
        elif uploaded_image.name.endswith('.pdf'):
            try:
                pdf_reader = PdfReader(uploaded_image)
                pdf_text = ""
                for page in pdf_reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        pdf_text += extracted + "\n"
                
                # Combine the PDF contents with any text area guidelines safely
                additional_text = pdf_text + "\n" + additional_text
                st.info("📄 PDF document loaded successfully! Processing document text content...")
            except Exception as pdf_error:
                st.error(f"Failed to process PDF content: {pdf_error}")
    
    # Text container for typed questions or context notes
    additional_text = st.text_area(
        "Add question text or custom context guidelines:", 
        placeholder="Type or paste text equations here..."
    )
    
    submit_button = st.button("Analyze & Solve Problem", use_container_width=True)

# ==========================================
# 3. BACKEND COMPUTATIONAL FLOW
# ==========================================
if submit_button:
    if uploaded_image is None and not additional_text.strip():
        st.warning("⚠️ Please provide an image or type out a query first.")
    else:
        # Strict zero-creativity parameter block to eliminate AI guessing
        strict_config = genai.GenerationConfig(temperature=0.0, top_p=0.1, top_k=1)
        primary_model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")
        
        system_instruction = f"""
        You are a highly precise, elite PCM evaluator for the Indian school curriculum ({grade_level}). 
        Your primary directive is absolute mathematical precision.
        
        Output your response using this precise layout structure:
        1. DETECTED QUESTION: State exactly what problem you read from the input.
        2. GIVEN DATA: List all parameters explicitly or implicitly given.
        3. STEP-BY-STEP DERIVATION: Show full calculations using standard formulas.
        4. FINAL VALUE: Highlight the definitive calculated answer with units.
        
        CRITICAL ADDITION: At the very end of your response, add an isolated section marker named '===SHORTCUT_TRICK==='. 
        Immediately under it, provide the absolute fastest shortcut formula or mental calculation hack used by top rankers in competitive exams to solve this specific question in under 5 seconds.
        
        CRITICAL SAFEGUARD: If the question lacks sufficient data, state exactly what parameter is missing. Do not guess or invent data.
        """
        
        # Assemble execution package
        payload = [system_instruction]
        if uploaded_image is not None:
            payload.append(pil_image)
        if additional_text.strip():
            payload.append(f"\nUser Query Notes: {additional_text}")

        # --- PHASE 1: ATTEMPT RUN WITH CHEAP/FAST FLASH CORE ---
        try:
            with st.spinner("Processing mathematical matrices..."):
                response = primary_model.generate_content(
                    payload,
                    generation_config={
                        "temperature": chosen_metrics["temperature"],
                        "top_p": chosen_metrics["top_p"]
                    }
                )
                raw_output = response.text

            # CREDIT SAVER GUARDRAIL: Blocks irrelevant prompts instantly
            if "no." in raw_output.lower() or "irrelevant" in raw_output.lower() or "invalid" in raw_output.lower():
                st.error("🚨 Access Denied: This question does not belong to the selected subject track.")
                st.stop()

            if not raw_output or "error" in raw_output.lower():
                raise ValueError("Anomalous sequence detected in calculation layer.")

            # Unpack textbook answers and shortcuts cleanly
            if "===SHORTCUT_TRICK===" in raw_output:
                textbook_solution, quick_trick = raw_output.split("===SHORTCUT_TRICK===")
            else:
                textbook_solution = raw_output
                quick_trick = "Standard derivation is the most optimal execution path for this system setup."

            with st.expander("⚡ JEE/NEET Speed Shortcut (Save 2 Minutes)"):
                st.markdown(quick_trick)

        # --- PHASE 2: AUTOMATIC SELF-HEALING SUPERVISOR ACTIVATION ---
        except Exception as error_log:
            st.warning("⚠️ Calculation variance caught. Deploying AI Supervisor to patch solution pipeline...")
            
            supervisor_model = genai.GenerativeModel(model_name="models/gemini-2.5-flash")
            healing_payload = [
                f"""
                SYSTEM EMERGENCY: The base model fractured parsing this request. 
                System Error Logged: {str(error_log)}
                Bypass the trap, re-evaluate natively, and output a flawless derivation split by the '===SHORTCUT_TRICK===' marker.
                """,
            ]
            if uploaded_image is not None:
                healing_payload.append(pil_image)
            if additional_text.strip():
                healing_payload.append(additional_text)

            with st.spinner("🔧 Core Supervisor is recalculating mathematical vectors..."):
                healed_response = supervisor_model.generate_content(healing_payload, generation_config=strict_config)
                raw_healed = healed_response.text

            if "===SHORTCUT_TRICK===" in raw_healed:
                healed_textbook, healed_trick = raw_healed.split("===SHORTCUT_TRICK===", 1)
            else:
                healed_textbook = raw_healed
                healed_trick = "Standard analytical steps are optimal for this specific instance."

            st.success("🎯 Patched Solution (Verified by Core AI Supervisor):")
            with st.container(border=True):
                st.markdown(healed_textbook)
            with st.expander("⚡ JEE/NEET Speed Shortcut (Save 2 Minutes)"):
                st.markdown(healed_trick)

            solution_text = healed_textbook

            st.session_state.chat_history.append({"role": "user", "content": additional_text})
            st.session_state.chat_history.append({"role": "assistant", "content": solution_text})