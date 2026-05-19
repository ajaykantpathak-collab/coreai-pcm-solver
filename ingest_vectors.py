import os
import requests
from io import BytesIO
from pypdf import PdfReader
import chromadb

def build_coreai_vector_moat():
    # This creates a folder named 'coreai_vector_vault' right next to your code
    chroma_client = chromadb.PersistentClient(path="./coreai_vector_vault")
    collection = chroma_client.get_or_create_collection(name="syllabus_moat")
    
    target_repositories = {
        "JEE_2014_Physics_P1": "https://raw.githubusercontent.com/imnikhilanand/IIT-JEE-paper-analysis/master/2014/Physics/Paper1.pdf",
        "JEE_2014_Chemistry_P1": "https://raw.githubusercontent.com/imnikhilanand/IIT-JEE-paper-analysis/master/2014/Chemistry/Paper1.pdf"
    }
    
    print("📡 Connection established. Streaming documents from GitHub into vectors...")
    
    for asset_id, download_url in target_repositories.items():
        try:
            response = requests.get(download_url, timeout=15)
            if response.status_code == 200:
                pdf_file = BytesIO(response.content)
                reader = PdfReader(pdf_file)
                
                extracted_content = ""
                for page in reader.pages:
                    extracted_content += page.extract_text() or ""
                
                collection.add(
                    documents=[extracted_content],
                    metadatas=[{"origin_node": "GitHub_CDN", "field_label": asset_id}],
                    ids=[asset_id]
                )
                print(f"✅ Context Indexed: {asset_id}")
        except Exception as e:
            print(f"⚠️ Error processing {asset_id}: {e}")

    print("🏁 System fully populated! Vector vault is locked and grounded.")

if __name__ == "__main__":
    build_coreai_vector_moat()