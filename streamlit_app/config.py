"""Configuration and constants for the RAG system"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file. Please create a .env file with your API key.")

# Paths
BASE_PATH = Path(__file__).parent
DATA_FOLDER = BASE_PATH / 'data'
VECTOR_STORE_PATH = BASE_PATH / 'vector_store'
DOCX_FILE = DATA_FOLDER / 'Ravi_Total.docx'

# Create directories if they don't exist
DATA_FOLDER.mkdir(exist_ok=True)
VECTOR_STORE_PATH.mkdir(exist_ok=True)

# LLM Configuration
LLM_MODEL = "llama-3.1-8b-instant"
LLM_TEMPERATURE = 0.3
LLM_MAX_TOKENS = 256

# Embeddings Configuration
EMBEDDINGS_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# RAG Configuration
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
RETRIEVER_K = 3

# System Configuration
SYSTEM_NAME = "Ravikumar HR Assistant"
