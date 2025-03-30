import os
import pytesseract
from pdf2image import convert_from_path
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
from PyPDF2 import PdfReader

# Load environment variables
load_dotenv()

# Set Tesseract Path if needed (for OCR processing of scanned PDFs)
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\shriy\AppData\Local\Programs\Tesseract-OCR"

# Define all PDF paths
DATA_PATHS = [
    r"C:\Users\shriy\Documents\Personal projects\allchapters.pdf",
    r"C:\Users\shriy\Documents\Personal projects\Diabetes_in_children_and_young_adults_for_website.pdf",
    r"C:\Users\shriy\Documents\Personal projects\paediatric-type-1-diabetes-resource-pack.pdf",
    r"C:\Users\shriy\Documents\Personal projects\type-1-diabetes-manual.pdf",
    r"C:\Users\shriy\Downloads\Smart Womans Guide to Diabetes.pdf",
    r"C:\Users\shriy\Downloads\DIA_Ch11.pdf",
    r"C:\Users\shriy\Downloads\pe22_mental_health_fnl_v_2.pdf",
    r"C:\Users\shriy\Downloads\sci-advisor_2018_nerve_damage-newb-final_v1.pdf",
    r"C:\Users\shriy\Downloads\sci-advisor_2018_skin_care_and_infections_v3.pdf",
    r"C:\Users\shriy\Downloads\checking_blood_glucose.pdf",
    r"C:\Users\shriy\Documents\Personal projects\type-1-diabetes-mellitus--pir.pdf"
]

# Function to load and standardize text from PDFs
def load_pdf_file(file_path):
    try:
        text = ""
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() or ""
        
        # If no text is extracted, try OCR (for scanned PDFs)
        if not text.strip():
            images = convert_from_path(file_path)
            text = "\n".join([pytesseract.image_to_string(img) for img in images])
        
        return text
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return ""

# Load and combine all PDFs
all_text = "\n".join([load_pdf_file(path) for path in DATA_PATHS])

# Standardize text (remove extra spaces and symbols)
def clean_text(text):
    text = text.replace("\n", " ").replace("\t", " ")  # Remove new lines/tabs
    text = " ".join(text.split())  # Normalize spaces
    return text

all_text = clean_text(all_text)

# Split text into chunks for better processing
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
text_chunks = text_splitter.create_documents([all_text])

# Create vector embeddings
def get_embedding_model():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

embedding_model = get_embedding_model()

# Store embeddings in FAISS
DB_FAISS_PATH = r"C:\Users\shriy\Documents\Personal projects\T1D_ASSISTANT\memory\faiss_db"
db = FAISS.from_documents(text_chunks, embedding_model)
db.save_local(DB_FAISS_PATH)

print("✅ Memory Created Successfully!")
