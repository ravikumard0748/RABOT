Streamlit App for Multi-Agent RAG System

## 📋 Project Structure

```
streamlit_app/
├── app.py                    # Main Streamlit application
├── config.py                 # Configuration and constants
├── agents.py                 # Validation & RAG agent logic
├── orchestrator.py          # Multi-agent orchestrator
├── setup.py                 # One-time setup script
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
├── .env                     # (Create this with your API key)
├── README.md                # This file
├── data/                    # Input data folder
│   └── Ravi_Total.docx     # Your document (add this)
└── vector_store/            # Vector store (auto-created)
    └── faiss_index/        # FAISS index (auto-created)
```

## 🚀 Setup Instructions

### 1. Create Environment File
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your Groq API key
# GROQ_API_KEY=your_api_key_here
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Add Your Document
- Place `Ravi_Total.docx` in the `data/` folder

### 4. Run Setup Script (One-Time)
```bash
python setup.py
```

This will:
- Load your document
- Split it into chunks (500 characters, 100 overlap)
- Create embeddings
- Save the FAISS vector store for reuse

### 5. Run Streamlit App
```bash
streamlit run app.py
```

The app will be available at: `http://localhost:8501`

## 📊 Features

### Ask Question Tab
- Ask professional questions about Ravikumar
- Get validation results (HR-appropriate check)
- View generated answers with source context
- See example questions for inspiration

### Statistics Tab
- View system statistics (total queries, success rate, etc.)
- Check system configuration (LLM, embeddings, etc.)
- Monitor performance metrics

### Query History Tab
- View all past queries
- Review answers and validation results
- Clear history if needed

### About Tab
- Learn how the system works
- Understand the technology stack
- View system information

## 🔄 How It Works

### One-Time Setup
1. **Document Loading**: Read `Ravi_Total.docx`
2. **Chunking**: Split document into 500-character chunks
3. **Embeddings**: Generate embeddings using HuggingFace model
4. **Vector Store**: Save FAISS index for reuse

### Query Processing
1. **Validation**: Check if question is HR-appropriate
2. **Retrieval**: Find relevant chunks from vector store
3. **Generation**: Use LLM to generate answer based on context
4. **Response**: Return answer with validation details

## 🛠️ Configuration

Edit `config.py` to customize:
```python
LLM_MODEL = "llama-3.1-8b-instant"  # Groq model
LLM_TEMPERATURE = 0.3                # Response creativity
CHUNK_SIZE = 500                      # Document chunk size
RETRIEVER_K = 3                       # Top K results to retrieve
```

## 📦 Key Components

### `app.py`
Streamlit UI with 4 tabs:
- Ask Question
- Statistics
- Query History
- About

### `config.py`
Centralized configuration for paths and settings

### `setup.py`
One-time setup script for creating vector store

### `agents.py`
- **Validation Agent**: Checks if questions are HR-appropriate
- **RAG Agent**: Retrieves and answers questions

### `orchestrator.py`
- Coordinates agents
- Loads pre-computed vector store
- Manages query history

## ✨ Key Features

✅ **One-Time Chunking**: Document is chunked once, vector store is reused
✅ **Privacy-Aware**: Validation agent ensures HR-appropriate questions
✅ **RAG System**: Retrieves only relevant information for accuracy
✅ **Persistent Storage**: Vector store is saved locally
✅ **User-Friendly**: Streamlit interface with multiple tabs
✅ **History Tracking**: Keep track of all queries and answers

## 🔐 Important Notes

- Add your `Ravi_Total.docx` to the `data/` folder
- Create `.env` with your `GROQ_API_KEY`
- Run `setup.py` once before using the app
- Vector store is reused for all queries (efficient!)
- All data is processed locally

## 🐛 Troubleshooting

**Vector store not found:**
```bash
python setup.py
```

**API key error:**
- Check `.env` file exists
- Verify `GROQ_API_KEY` is set correctly

**Import errors:**
```bash
pip install -r requirements.txt
```

**Streamlit not starting:**
```bash
streamlit run app.py --logger.level=debug
```

## 📝 Usage Example

```python
# In the app:
1. Go to "Ask Question" tab
2. Type: "What are Ravikumar's technical skills?"
3. Click "Send"
4. View validation result and answer
5. Check "Query History" to see past questions
```

## 🎯 Next Steps

- Customize the system prompt in `agents.py`
- Adjust chunk size/overlap in `config.py`
- Add more documents to the vector store
- Deploy to cloud (Streamlit Cloud, Azure, etc.)

---

**Happy questioning! 🤖**
