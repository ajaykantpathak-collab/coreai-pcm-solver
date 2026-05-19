import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import chromadb

app = FastAPI(title="CoreAI Compute Engine Node")

#  Updated Initialization (Fine-Tuned for Strict PCM Math)
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# Define the calibration parameters
tuned_settings = {
    "temperature": 0.0,         # Eliminates creative guesswork and forces deterministic logic
    "top_p": 0.95,
    "max_output_tokens": 4096,   # Expands room for complex, long step-by-step LaTeX derivations
}

# Pass the settings directly into the model instance
model = genai.GenerativeModel(
    model_name="models/gemini-2.5-flash",
    generation_config=tuned_settings
)

# 🔍 Connect to your pre-computed vector database folder
chroma_client = chromadb.PersistentClient(path="./coreai_vector_vault")
collection = chroma_client.get_or_create_collection(name="syllabus_moat")

class StudentQuery(BaseModel):
    prompt: str

@app.post("/v1/compute/solve")
async def process_student_doubt(payload: StudentQuery):
    try:
        # 1. Search the local vector store for matching textbook/paper context
        results = collection.query(
            query_texts=[payload.prompt],
            n_results=4
        )
        
        # Extract matching text snippets if found
        context = ""
        if results and results['documents'] and results['documents'][0]:
            context = results['documents'][0][0][:2000] # Grab first 2000 chars of relevant context
            
        # 2. Build a grounded prompt forcing the AI to stick to official syllabus materials
        grounded_prompt = f"""
        You are an elite, hyper-accurate PCM tutor for JEE/NEET. 
        Use the following official syllabus context to answer the student's question accurately.
        If the context doesn't help, use your deep physics/chemistry/math knowledge.
        Always format equations beautifully in standard LaTeX using $ for inline math and $$ for blocks.
        
        [Syllabus Context]:
        {context}
        
        [Student Question]:
        {payload.prompt}
        """
        
        if not api_key:
            return {"status": "offline_testing", "payload": "Backend alive! Context search working perfectly."}
            
        response = model.generate_content(grounded_prompt)
        return {"status": "success", "payload": response.text}
        
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)