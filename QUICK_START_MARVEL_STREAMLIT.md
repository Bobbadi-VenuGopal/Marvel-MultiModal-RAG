# 🦸 Quick Start - Marvel Streamlit App

## Run the Marvel Streamlit App

### Step 1: Install Dependencies (if needed)

```bash
pip install streamlit
```

### Step 2: Start Ollama (for AI responses)

```bash
# Start Ollama server
ollama serve

# In another terminal, pull the model (if not already done)
ollama pull mistral:7b
```

### Step 3: Set Up Marvel Vector Database (Optional)

```bash
# Create Marvel content
python marvel_vector_db/scripts/1_fetch_marvel_documents.py

# Process and create vector database
python marvel_vector_db/scripts/4_process_marvel_content.py
```

### Step 4: Run the Streamlit App

```bash
# Windows
streamlit run marvel_streamlit_app.py

# Or use the batch file
run_marvel_streamlit.bat

# The app will open in your browser at http://localhost:8501
```

## What You Can Do

### 1. Query Marvel Knowledge Base
- Ask questions about Marvel characters
- Learn about storylines and events
- Get information about teams and comics

### 2. Chat with Documents
- Load processed Marvel documents
- Ask questions about document content
- Get detailed Marvel-focused responses

### 3. Chat with Audio
- Load processed Marvel audio files
- Ask questions about audio content
- Get summaries and insights

### 4. View System Status
- Check Ollama status
- View loaded documents and audio
- Monitor Marvel vector database

## Example Questions

**Marvel Knowledge Base:**
- "What are Spider-Man's powers?"
- "Tell me about the Infinity Gauntlet"
- "Who are the founding members of the Avengers?"
- "Describe the Civil War event"

**Documents:**
- "What Marvel characters are mentioned in this document?"
- "What storylines are discussed?"
- "Tell me about the events described"

**Audio:**
- "What Marvel content was discussed?"
- "Who are the characters mentioned?"
- "What storylines were covered?"

## Troubleshooting

### App won't start
```bash
# Check if Streamlit is installed
pip install streamlit

# Try running directly
python -m streamlit run marvel_streamlit_app.py
```

### Ollama not working
```bash
# Check if Ollama is running
curl http://localhost:11434/

# Start Ollama
ollama serve
```

### Marvel DB not loading
```bash
# Run setup scripts
python marvel_vector_db/scripts/1_fetch_marvel_documents.py
python marvel_vector_db/scripts/4_process_marvel_content.py
```

## Features

✅ Marvel-themed UI with red/orange/yellow colors  
✅ Query Marvel knowledge base  
✅ Chat with documents and audio  
✅ AI-powered responses with Marvel context  
✅ System status monitoring  
✅ Beautiful Marvel-themed interface  

## Enjoy!

The app is ready to use. Just run `streamlit run marvel_streamlit_app.py` and start exploring Marvel content! 🦸

