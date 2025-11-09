# 🦸 Marvel Streamlit App - Setup Guide

## Overview

The Marvel Streamlit App provides a web interface for the Marvel Multimodal RAG System. It allows you to:

- Query the Marvel knowledge base
- Chat with processed Marvel documents
- Chat with processed Marvel audio files
- View system status and metrics

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
pip install streamlit
```

### 2. Set Up Ollama (for AI responses)

```bash
# Install Ollama from https://ollama.com/
# Then start Ollama:
ollama serve

# Pull the Mistral model:
ollama pull mistral:7b
```

### 3. Set Up Marvel Vector Database (Optional but Recommended)

```bash
# Run the document fetcher:
python marvel_vector_db/scripts/1_fetch_marvel_documents.py

# Process the content:
python marvel_vector_db/scripts/4_process_marvel_content.py
```

## Running the App

### Windows

```bash
# Option 1: Use the batch file
run_marvel_streamlit.bat

# Option 2: Run directly
streamlit run marvel_streamlit_app.py
```

### Linux/Mac

```bash
# Option 1: Use the shell script
chmod +x run_marvel_streamlit.sh
./run_marvel_streamlit.sh

# Option 2: Run directly
streamlit run marvel_streamlit_app.py
```

### Python

```bash
python -m streamlit run marvel_streamlit_app.py
```

## Features

### 1. 🦸 Marvel Knowledge Base

- Query the Marvel vector database
- Ask questions about characters, storylines, events
- Get AI-powered responses with Marvel context

**Example Questions:**
- "What are Spider-Man's powers?"
- "Tell me about the Infinity Gauntlet event"
- "Who are the founding members of the Avengers?"
- "Describe the Civil War storyline"

### 2. 📄 Documents

- Load and chat with processed Marvel documents
- Upload PDFs with Marvel content
- Get detailed answers about document content

### 3. 🎵 Audio

- Load and chat with processed Marvel audio files
- Ask questions about audio transcriptions
- Get summaries and insights from audio content

### 4. 📊 System Status

- View system metrics
- Check Ollama status
- Monitor loaded documents and audio files
- View Marvel vector database status

## Interface Pages

1. **🦸 Marvel Knowledge**: Query the Marvel knowledge base
2. **📄 Documents**: Chat with processed documents
3. **🎵 Audio**: Chat with processed audio files
4. **📊 System Status**: View system metrics and status

## Troubleshooting

### Ollama Not Running

```bash
# Start Ollama
ollama serve

# Check if it's running
curl http://localhost:11434/
```

### Marvel Vector Database Not Loaded

```bash
# Run the setup scripts
python marvel_vector_db/scripts/1_fetch_marvel_documents.py
python marvel_vector_db/scripts/4_process_marvel_content.py

# Then refresh the Streamlit app
```

### Streamlit Not Found

```bash
# Install Streamlit
pip install streamlit

# Verify installation
streamlit --version
```

### Port Already in Use

```bash
# Run on a different port
streamlit run marvel_streamlit_app.py --server.port 8502
```

## Configuration

### Change Port

```bash
streamlit run marvel_streamlit_app.py --server.port 8502
```

### Change Host

```bash
streamlit run marvel_streamlit_app.py --server.address 0.0.0.0
```

### Enable Sharing

```bash
streamlit run marvel_streamlit_app.py --server.enableCORS false --server.enableXsrfProtection false
```

## Marvel-Themed UI

The app features a Marvel-themed interface with:
- Red, orange, and yellow gradient colors (Marvel colors)
- Character-themed styling
- Marvel-specific prompts and responses
- Comic book-inspired design

## Integration

The Streamlit app integrates with:
- Marvel vector database (`marvel_vector_db/vectorstore/`)
- Preprocessed documents (`preprocessed_documents/`)
- Preprocessed audio (`preprocessed_audio/`)
- Ollama for AI responses
- ChromaDB for vector storage

## Next Steps

1. **Set up Marvel vector database**: Run the setup scripts
2. **Process documents**: Upload and process Marvel documents
3. **Process audio**: Upload and process Marvel audio files
4. **Query the knowledge base**: Ask questions about Marvel content
5. **Explore the interface**: Try different pages and features

## Support

For issues or questions:
1. Check the troubleshooting section
2. Verify all dependencies are installed
3. Check that Ollama is running
4. Ensure the Marvel vector database is set up correctly

## Notes

- The app requires Ollama to be running for AI responses
- The Marvel vector database is optional but recommended
- Preprocessed documents and audio are loaded automatically
- The app uses Marvel-specific prompts for better responses

