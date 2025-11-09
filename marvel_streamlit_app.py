import streamlit as st
import os
import json
import pickle
import time
import sys
from datetime import datetime
from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.storage import InMemoryStore
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain.schema.document import Document
import requests
import torch

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        if sys.stdout.encoding != 'utf-8':
            sys.stdout.reconfigure(encoding='utf-8')
        if sys.stderr.encoding != 'utf-8':
            sys.stderr.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, errors='replace')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, errors='replace')

# Page configuration
st.set_page_config(
    page_title="🦸 Marvel Multimodal RAG System",
    page_icon="🦸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Marvel-themed UI
st.markdown("""
    <style>
    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Marvel-themed header */
    .main-header {
        background: linear-gradient(135deg, #d32f2f 0%, #f57c00 50%, #fbc02d 100%);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(211, 47, 47, 0.3);
        border: 3px solid #fff;
    }
    
    .main-header h1 {
        color: white;
        font-size: 3rem;
        margin: 0;
        font-weight: 800;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
    }
    
    /* Status cards */
    .status-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 1.5rem;
        border-radius: 16px;
        border: 2px solid #d32f2f;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .status-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #d32f2f 0%, #f57c00 50%, #fbc02d 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Chat messages */
    .user-message {
        background: linear-gradient(135deg, #d32f2f 0%, #f57c00 50%, #fbc02d 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 18px;
        margin: 1rem 0;
        margin-left: 20%;
        border-bottom-right-radius: 4px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .bot-message {
        background: #334155;
        color: #f1f5f9;
        padding: 1rem 1.5rem;
        border-radius: 18px;
        margin: 1rem 0;
        margin-right: 20%;
        border-bottom-left-radius: 4px;
        border: 2px solid #d32f2f;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom button styling */
    .stButton > button {
        background: linear-gradient(135deg, #d32f2f 0%, #f57c00 50%, #fbc02d 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(211, 47, 47, 0.4);
    }
    
    /* Marvel-themed metrics */
    .marvel-metric {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 1rem;
        border-radius: 12px;
        border: 2px solid #d32f2f;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'preprocessed_docs' not in st.session_state:
    st.session_state.preprocessed_docs = {}
if 'preprocessed_audio' not in st.session_state:
    st.session_state.preprocessed_audio = {}
if 'embeddings' not in st.session_state:
    st.session_state.embeddings = None
if 'doc_messages' not in st.session_state:
    st.session_state.doc_messages = []
if 'audio_messages' not in st.session_state:
    st.session_state.audio_messages = []
if 'selected_doc' not in st.session_state:
    st.session_state.selected_doc = None
if 'selected_audio' not in st.session_state:
    st.session_state.selected_audio = None
if 'marvel_vector_db' not in st.session_state:
    st.session_state.marvel_vector_db = None

# Initialize models
@st.cache_resource
def load_embeddings():
    """Load embeddings model"""
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-large-en-v1.5",
            model_kwargs={"device": "cpu"}
        )
        return embeddings
    except Exception as e:
        st.error(f"Error loading embeddings: {e}")
        return None

# Check Ollama
def check_ollama():
    """Check if Ollama is running"""
    try:
        response = requests.get("http://localhost:11434/", timeout=3)
        return response.status_code == 200
    except:
        return False

# Query Mistral with Marvel context
def query_mistral_marvel(prompt):
    """Query Mistral with Marvel-focused responses"""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral:7b",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.2,
                    "top_k": 40,
                    "top_p": 0.9,
                    "num_predict": 400,
                    "num_ctx": 2048,
                }
            },
            timeout=25
        )
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result.get("response", "").strip()
            if ai_response and len(ai_response) > 20:
                return ai_response
        return None
    except Exception as e:
        st.error(f"Mistral query failed: {e}")
        return None

# Load Marvel vector database
def load_marvel_vector_db():
    """Load Marvel vector database from marvel_vector_db folder"""
    vectorstore_path = Path("marvel_vector_db/vectorstore")
    
    if not vectorstore_path.exists():
        return None
    
    try:
        if st.session_state.embeddings:
            vectorstore = Chroma(
                collection_name="marvel_knowledge_base",
                embedding_function=st.session_state.embeddings,
                persist_directory=str(vectorstore_path)
            )
            return vectorstore
    except Exception as e:
        st.warning(f"Could not load Marvel vector database: {e}")
    
    return None

# Load preprocessed content
def load_preprocessed_content():
    """Load all pre-processed content"""
    docs_dir = "./preprocessed_documents"
    audio_dir = "./preprocessed_audio"
    
    # Load documents
    if os.path.exists(docs_dir):
        doc_folders = [f for f in os.listdir(docs_dir) 
                      if os.path.isdir(os.path.join(docs_dir, f)) and not f.startswith('.')]
        for file_id in doc_folders:
            doc_path = os.path.join(docs_dir, file_id)
            try:
                metadata_path = os.path.join(doc_path, "metadata.json")
                if os.path.exists(metadata_path):
                    with open(metadata_path, 'r') as f:
                        metadata = json.load(f)
                else:
                    metadata = {"text_count": 0, "table_count": 0, "image_count": 0}

                doc_data_path = os.path.join(doc_path, "document_data.pkl")
                if os.path.exists(doc_data_path):
                    with open(doc_data_path, 'rb') as f:
                        doc_data = pickle.load(f)
                    st.session_state.preprocessed_docs[file_id] = {
                        "metadata": metadata,
                        "doc_data": doc_data
                    }
            except Exception as e:
                st.warning(f"Error loading document {file_id}: {e}")
    
    # Load audio
    if os.path.exists(audio_dir):
        audio_folders = [f for f in os.listdir(audio_dir) 
                        if os.path.isdir(os.path.join(audio_dir, f)) and not f.startswith('.')]
        for file_id in audio_folders:
            audio_path = os.path.join(audio_dir, file_id)
            try:
                audio_data_path = os.path.join(audio_path, "audio_data.json")
                if os.path.exists(audio_data_path):
                    with open(audio_data_path, 'r') as f:
                        audio_data = json.load(f)
                    st.session_state.preprocessed_audio[file_id] = audio_data
            except Exception as e:
                st.warning(f"Error loading audio {file_id}: {e}")

# Initialize
if st.session_state.embeddings is None:
    with st.spinner("Loading embeddings model..."):
        st.session_state.embeddings = load_embeddings()

# Load Marvel vector database
if st.session_state.marvel_vector_db is None:
    with st.spinner("Loading Marvel vector database..."):
        st.session_state.marvel_vector_db = load_marvel_vector_db()

if not st.session_state.preprocessed_docs and not st.session_state.preprocessed_audio:
    with st.spinner("Loading preprocessed content..."):
        load_preprocessed_content()

# Header
st.markdown("""
    <div class="main-header">
        <h1>🦸 Marvel Multimodal RAG System</h1>
        <p>Marvel Comics Knowledge Base - AI-Powered Document & Audio Assistant</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🦸 System Status")
    
    ollama_status = check_ollama()
    doc_count = len(st.session_state.preprocessed_docs)
    audio_count = len(st.session_state.preprocessed_audio)
    marvel_db_loaded = st.session_state.marvel_vector_db is not None
    
    st.metric("Documents", doc_count)
    st.metric("Audio Files", audio_count)
    st.metric("Marvel DB", "Loaded" if marvel_db_loaded else "Not Loaded")
    
    if ollama_status:
        st.success("✅ Ollama: Online")
    else:
        st.warning("⚠️ Ollama: Offline")
        st.info("To enable AI queries, start Ollama:\n```\nollama serve\nollama pull mistral:7b\n```")
    
    st.markdown("---")
    st.markdown("### 🎯 Navigation")
    page = st.radio("Select Page", ["🦸 Marvel Knowledge", "📄 Documents", "🎵 Audio", "📊 System Status"])

# Main content
if page == "🦸 Marvel Knowledge":
    st.markdown("## 🦸 Marvel Comics Knowledge Base")
    
    if st.session_state.marvel_vector_db:
        st.success("✅ Marvel vector database loaded! Ask questions about Marvel characters, storylines, and events.")
        
        # Marvel knowledge chat
        st.markdown("### 💬 Chat with Marvel Knowledge Base")
        
        # Display messages
        if st.session_state.doc_messages:
            for message in st.session_state.doc_messages:
                if message['type'] == 'user':
                    st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(message["content"], unsafe_allow_html=True)
        else:
            st.info("👋 Ask questions about Marvel characters, storylines, comics, teams, or events!")
            st.markdown("**Example questions:**")
            st.markdown("- What are Spider-Man's powers?")
            st.markdown("- Tell me about the Infinity Gauntlet event")
            st.markdown("- Who are the founding members of the Avengers?")
            st.markdown("- Describe the Civil War storyline")
        
        # Query input
        query = st.text_input("Ask about Marvel:", key="marvel_query_input", 
                             placeholder="What Marvel character or storyline would you like to know about?")
        col1, col2 = st.columns([1, 4])
        with col1:
            send_button = st.button("Send", type="primary", use_container_width=True)
        
        if send_button and query:
            # Add user message
            st.session_state.doc_messages.append({'type': 'user', 'content': query})
            
            # Query Marvel vector database
            with st.spinner("Searching Marvel knowledge base..."):
                try:
                    # Search vector database
                    results = st.session_state.marvel_vector_db.similarity_search(query, k=3)
                    
                    # Combine context
                    context = "\n\n".join([doc.page_content for doc in results])
                    
                    # Query AI with Marvel context
                    ai_response = None
                    if check_ollama() and context:
                        prompt = f"""You are a Marvel Comics expert assistant. Answer the following question about Marvel characters, storylines, comics, or universe based on the provided context.

Context from Marvel knowledge base:
{context[:2000]}

Question: {query}

Please provide a comprehensive answer focusing on:
- Specific character names, powers, and storylines
- Marvel universe details and events
- Comic book history and notable storylines
- Team affiliations and relationships

Use markdown formatting for better readability (headers, lists, bold text).

Detailed Answer:"""
                        
                        ai_response = query_mistral_marvel(prompt)
                    
                    if not ai_response:
                        ai_response = f"**Marvel Knowledge Base Response**\n\n**Question:** {query}\n\n**Relevant Context Found:**\n\n{context[:1000]}\n\n*AI analysis temporarily unavailable. Please ensure Ollama is running.*"
                    
                    st.session_state.doc_messages.append({'type': 'bot', 'content': ai_response})
                    st.rerun()
                    
                except Exception as e:
                    error_msg = f"**Error:** {str(e)}\n\n*Please check if the Marvel vector database is properly set up.*"
                    st.session_state.doc_messages.append({'type': 'bot', 'content': error_msg})
                    st.rerun()
        
        # Clear chat button
        if st.button("Clear Chat", key="clear_marvel_chat"):
            st.session_state.doc_messages = []
            st.rerun()
    
    else:
        st.warning("⚠️ Marvel vector database not loaded.")
        st.info("""
        **To set up the Marvel vector database:**
        
        1. Run the document fetcher:
           ```bash
           python marvel_vector_db/scripts/1_fetch_marvel_documents.py
           ```
        
        2. Process the content:
           ```bash
           python marvel_vector_db/scripts/4_process_marvel_content.py
           ```
        
        3. Refresh this page to load the database.
        """)

elif page == "📄 Documents":
    st.markdown("## 📄 Marvel Document Chat")
    
    # Document selection
    if st.session_state.preprocessed_docs:
        doc_options = list(st.session_state.preprocessed_docs.keys())
        selected_doc = st.selectbox(
            "Select a document",
            options=doc_options,
            index=0 if st.session_state.selected_doc is None else doc_options.index(st.session_state.selected_doc) if st.session_state.selected_doc in doc_options else 0
        )
        st.session_state.selected_doc = selected_doc
        
        # Display document info
        if selected_doc:
            doc_data = st.session_state.preprocessed_docs[selected_doc]
            metadata = doc_data.get('metadata', {})
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Text Chunks", metadata.get('text_count', 0))
            with col2:
                st.metric("Tables", metadata.get('table_count', 0))
            with col3:
                st.metric("Images", metadata.get('image_count', 0))
        
        # Chat interface
        col_header1, col_header2 = st.columns([4, 1])
        with col_header1:
            st.markdown("### 💬 Chat")
        with col_header2:
            if st.button("Clear Chat", key="clear_doc_chat"):
                st.session_state.doc_messages = []
                st.rerun()
        
        # Display messages
        if st.session_state.doc_messages:
            for message in st.session_state.doc_messages:
                if message['type'] == 'user':
                    st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(message["content"], unsafe_allow_html=True)
        else:
            st.info("👋 Start a conversation by asking a question about the Marvel document!")
        
        # Query input
        query = st.text_input("Ask about the document:", key="doc_query_input",
                             placeholder="What Marvel characters or storylines are in this document?")
        col1, col2 = st.columns([1, 4])
        with col1:
            send_button = st.button("Send", type="primary", use_container_width=True)
        
        if send_button and query and selected_doc:
            # Add user message
            st.session_state.doc_messages.append({'type': 'user', 'content': query})
            
            # Query document
            with st.spinner("Thinking..."):
                doc_data = st.session_state.preprocessed_docs[selected_doc]
                
                # Extract content
                content_parts = []
                if 'doc_data' in doc_data:
                    doc_content = doc_data['doc_data']
                    if 'texts' in doc_content:
                        texts = doc_content['texts']
                        for text in texts[:5]:
                            text_str = str(text)
                            if len(text_str.strip()) > 20:
                                content_parts.append(text_str[:800])
                    elif 'text_chunks' in doc_content:
                        texts = doc_content['text_chunks']
                        for text in texts[:5]:
                            text_str = str(text)
                            if len(text_str.strip()) > 20:
                                content_parts.append(text_str[:800])
                
                combined_content = " ".join(content_parts)
                
                # Try vectorstore
                if not combined_content or len(combined_content.strip()) < 50:
                    vectorstore_path = os.path.join("./preprocessed_documents", selected_doc, "vectorstore")
                    if os.path.exists(vectorstore_path) and st.session_state.embeddings:
                        try:
                            vectorstore = Chroma(
                                persist_directory=vectorstore_path,
                                embedding_function=st.session_state.embeddings
                            )
                            if query:
                                results = vectorstore.similarity_search(query, k=3)
                                for result in results:
                                    content_parts.append(result.page_content[:800])
                                combined_content = " ".join(content_parts)
                        except Exception as e:
                            st.warning(f"Could not load from vectorstore: {e}")
                
                # Query AI with Marvel context
                ai_response = None
                if check_ollama() and combined_content:
                    prompt = f"""You are a Marvel Comics expert assistant. Analyze the following document content and provide a comprehensive, detailed answer to the user's question.

Document Name: {selected_doc}
Document Content: {combined_content[:2000]}

User Question: {query}

Please provide a thorough, well-structured response that:
1. Directly answers the question about Marvel content
2. Includes relevant details about characters, storylines, or events
3. Uses specific information from the document
4. Uses markdown formatting for better readability (headers, lists, bold text)

Format your response using markdown:
- Use **bold** for important points
- Use headers (##, ###) for sections
- Use bullet points or numbered lists

Detailed Answer:"""
                    
                    ai_response = query_mistral_marvel(prompt)
                
                if not ai_response:
                    ai_response = f"**Marvel Document Analysis**\n\nDocument: {selected_doc}\n\nQuestion: {query}\n\n*AI analysis temporarily unavailable. Please ensure Ollama is running.*"
                
                st.session_state.doc_messages.append({'type': 'bot', 'content': ai_response})
                st.rerun()
    else:
        st.info("No documents available. Please add documents to the preprocessed_documents folder.")

elif page == "🎵 Audio":
    st.markdown("## 🎵 Marvel Audio Chat")
    
    # Audio selection
    if st.session_state.preprocessed_audio:
        audio_options = list(st.session_state.preprocessed_audio.keys())
        selected_audio = st.selectbox(
            "Select an audio file",
            options=audio_options,
            index=0 if st.session_state.selected_audio is None else audio_options.index(st.session_state.selected_audio) if st.session_state.selected_audio in audio_options else 0
        )
        st.session_state.selected_audio = selected_audio
        
        # Display audio info
        if selected_audio:
            audio_data = st.session_state.preprocessed_audio[selected_audio]
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Chunks", audio_data.get('num_chunks', 0))
            with col2:
                st.metric("Transcript Length", f"{len(audio_data.get('transcript', '')):,} chars")
        
        # Chat interface
        col_header1, col_header2 = st.columns([4, 1])
        with col_header1:
            st.markdown("### 💬 Chat")
        with col_header2:
            if st.button("Clear Chat", key="clear_audio_chat"):
                st.session_state.audio_messages = []
                st.rerun()
        
        # Display messages
        if st.session_state.audio_messages:
            for message in st.session_state.audio_messages:
                if message['type'] == 'user':
                    st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(message["content"], unsafe_allow_html=True)
        else:
            st.info("👋 Start a conversation by asking a question about the Marvel audio!")
        
        # Query input
        query = st.text_input("Ask about the audio:", key="audio_query_input",
                             placeholder="What Marvel-related content was discussed in the audio?")
        col1, col2 = st.columns([1, 4])
        with col1:
            send_button = st.button("Send", type="primary", use_container_width=True, key="audio_send")
        
        if send_button and query and selected_audio:
            # Add user message
            st.session_state.audio_messages.append({'type': 'user', 'content': query})
            
            # Query audio
            with st.spinner("Thinking..."):
                audio_data = st.session_state.preprocessed_audio[selected_audio]
                transcript = audio_data.get('transcript', '')
                
                # Try vectorstore
                relevant_content = transcript
                vectorstore_path = os.path.join("./preprocessed_audio", selected_audio, "vectorstore")
                if os.path.exists(vectorstore_path) and st.session_state.embeddings:
                    try:
                        vectorstore = Chroma(
                            persist_directory=vectorstore_path,
                            embedding_function=st.session_state.embeddings
                        )
                        if query:
                            results = vectorstore.similarity_search(query, k=3)
                            relevant_chunks = [result.page_content for result in results]
                            if relevant_chunks:
                                relevant_content = " ".join(relevant_chunks[:3])
                    except Exception as e:
                        relevant_content = transcript[:2000]
                else:
                    relevant_content = transcript[:2000] if len(transcript) > 2000 else transcript
                
                # Query AI with Marvel context
                ai_response = None
                if check_ollama() and relevant_content:
                    prompt = f"""You are a Marvel Comics expert assistant. Analyze the following audio transcript and provide a comprehensive, detailed answer to the user's question.

Audio File: {selected_audio}
Transcript Content: {relevant_content[:2000]}

User Question: {query}

Please provide a thorough, well-structured response that:
1. Directly answers the question about Marvel-related audio content
2. Summarizes key topics and themes discussed
3. Provides specific details about characters, storylines, or events
4. Uses markdown formatting for better readability (headers, lists, bold text)

Detailed Analysis:"""
                    
                    ai_response = query_mistral_marvel(prompt)
                
                if not ai_response:
                    ai_response = f"**Marvel Audio Analysis**\n\nAudio: {selected_audio}\n\nQuestion: {query}\n\n*AI analysis temporarily unavailable. Please ensure Ollama is running.*"
                
                st.session_state.audio_messages.append({'type': 'bot', 'content': ai_response})
                st.rerun()
    else:
        st.info("No audio files available. Please add audio files to the preprocessed_audio folder.")

else:  # System Status
    st.markdown("## 📊 System Status")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Documents", len(st.session_state.preprocessed_docs))
    with col2:
        st.metric("Audio Files", len(st.session_state.preprocessed_audio))
    with col3:
        ollama_status = check_ollama()
        if ollama_status:
            st.metric("Ollama", "Online", delta="Running")
        else:
            st.metric("Ollama", "Offline", delta="Not Running", delta_color="inverse")
    
    st.markdown("---")
    
    # Marvel vector database status
    st.markdown("### 🦸 Marvel Vector Database")
    if st.session_state.marvel_vector_db:
        st.success("✅ Marvel vector database is loaded")
        try:
            count = st.session_state.marvel_vector_db._collection.count()
            st.metric("Documents in DB", count)
        except:
            st.info("Could not retrieve document count")
    else:
        st.warning("⚠️ Marvel vector database not loaded")
        st.info("Run the setup scripts in marvel_vector_db/scripts/ to create the database")
    
    st.markdown("---")
    
    # Documents list
    st.markdown("### 📄 Available Documents")
    if st.session_state.preprocessed_docs:
        for doc_id, doc_data in st.session_state.preprocessed_docs.items():
            metadata = doc_data.get('metadata', {})
            with st.expander(doc_id):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Text Chunks:** {metadata.get('text_count', 0)}")
                with col2:
                    st.write(f"**Tables:** {metadata.get('table_count', 0)}")
                with col3:
                    st.write(f"**Images:** {metadata.get('image_count', 0)}")
    else:
        st.info("No documents loaded")
    
    st.markdown("---")
    
    # Audio list
    st.markdown("### 🎵 Available Audio Files")
    if st.session_state.preprocessed_audio:
        for audio_id, audio_data in st.session_state.preprocessed_audio.items():
            with st.expander(audio_id):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Chunks:** {audio_data.get('num_chunks', 0)}")
                with col2:
                    st.write(f"**Transcript Length:** {len(audio_data.get('transcript', '')):,} chars")
    else:
        st.info("No audio files loaded")

