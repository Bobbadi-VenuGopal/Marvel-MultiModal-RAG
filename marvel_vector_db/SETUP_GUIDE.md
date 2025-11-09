# Marvel Vector Database - Setup Guide

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Scripts

Navigate to the `marvel_vector_db` directory and run scripts in order:

```bash
# From project root
cd marvel_vector_db

# Run from scripts directory
cd scripts
python 1_fetch_marvel_documents.py
python 2_fetch_marvel_images.py
python 3_fetch_marvel_audio.py
python 4_process_marvel_content.py
python 5_marvel_rag_query.py
```

### 3. Or Run Main Pipeline

```bash
cd marvel_vector_db/scripts
python 0_main_pipeline.py
```

## Script Descriptions

### 1. Document Fetcher (`1_fetch_marvel_documents.py`)
- Creates Marvel character, team, and event documents
- Saves to `raw_data/documents/`
- Creates metadata.json with file information

### 2. Image Fetcher Setup (`2_fetch_marvel_images.py`)
- Sets up image downloading structure
- Creates metadata and instructions
- You need to download images manually or update URLs

### 3. Audio Fetcher Setup (`3_fetch_marvel_audio.py`)
- Sets up audio downloading structure
- Creates metadata and instructions
- You need to download audio files manually or update URLs

### 4. Content Processor (`4_process_marvel_content.py`)
- Processes all content (documents, images, audio)
- Creates vector embeddings
- Stores in ChromaDB vector database

### 5. RAG Query Interface (`5_marvel_rag_query.py`)
- Interactive query interface
- Query the Marvel knowledge base
- Get answers about Marvel characters, storylines, etc.

## Directory Structure

```
marvel_vector_db/
├── raw_data/           # Raw downloaded content
│   ├── documents/      # Text files
│   ├── images/         # Image files
│   └── audio/          # Audio files
├── processed_data/     # Processed content
├── vectorstore/        # ChromaDB database
└── scripts/            # Processing scripts
```

## Next Steps

1. **Fetch Documents**: Run `1_fetch_marvel_documents.py` to create initial content
2. **Download Images**: Manually download Marvel images or update URLs in metadata
3. **Download Audio**: Manually download Marvel audio or update URLs in metadata
4. **Process Content**: Run `4_process_marvel_content.py` to create vector database
5. **Query Database**: Run `5_marvel_rag_query.py` to query the knowledge base

## Integration with Marvel Notebook

The vector database can be integrated with `multimodal_rag_final_marvel.ipynb`:

1. Process content using the scripts
2. Export the vectorstore
3. Load in the notebook for enhanced RAG capabilities

## Troubleshooting

- **Path Issues**: Make sure you're running scripts from the correct directory
- **Missing Dependencies**: Install all requirements from requirements.txt
- **Ollama Not Running**: Start Ollama server for LLM responses
- **Vector Database Not Found**: Run processing script first

## Notes

- Respect copyright when downloading content
- Be respectful with web scraping (rate limiting)
- Ensure sufficient disk space for vector database
- GPU optional but recommended for faster processing

