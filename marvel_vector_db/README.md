# Marvel Vector Database

A comprehensive vector database for Marvel Comics content including documents, images, and audio files with RAG (Retrieval-Augmented Generation) capabilities.

## 🎯 Overview

This project creates a vector database of Marvel Comics content that can be queried using RAG. It includes:

- **Documents**: Character bios, storylines, team information, and event descriptions
- **Images**: Character artwork, comic covers, and team lineups
- **Audio**: Podcasts, interviews, and discussions about Marvel content
- **RAG Interface**: Query the database with natural language questions

## 📁 Project Structure

```
marvel_vector_db/
├── raw_data/              # Raw downloaded content
│   ├── documents/         # Text documents
│   ├── images/            # Image files
│   └── audio/             # Audio files
├── processed_data/        # Processed content
│   ├── documents/         # Processed documents
│   ├── images/            # Processed images
│   └── audio/             # Processed audio
├── vectorstore/           # ChromaDB vector database
├── scripts/               # Processing scripts
│   ├── 0_main_pipeline.py        # Main pipeline orchestrator
│   ├── 1_fetch_marvel_documents.py  # Fetch documents
│   ├── 2_fetch_marvel_images.py     # Set up image fetching
│   ├── 3_fetch_marvel_audio.py      # Set up audio fetching
│   ├── 4_process_marvel_content.py  # Process and create vector DB
│   └── 5_marvel_rag_query.py        # RAG query interface
└── README.md              # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Ollama (for LLM)

```bash
# Install Ollama from https://ollama.com/
# Then pull the model:
ollama pull mistral:7b
ollama serve
```

### 3. Run the Pipeline

```bash
# Run the main pipeline
cd scripts
python 0_main_pipeline.py

# Or run individual scripts:
python 1_fetch_marvel_documents.py  # Fetch documents
python 2_fetch_marvel_images.py     # Set up image fetching
python 3_fetch_marvel_audio.py      # Set up audio fetching
python 4_process_marvel_content.py  # Process content
```

### 4. Query the Database

```bash
python 5_marvel_rag_query.py
```

## 📋 Detailed Instructions

### Step 1: Fetch Documents

The document fetcher creates Marvel content from known information:

```bash
python scripts/1_fetch_marvel_documents.py
```

This creates text files with information about:
- Marvel characters (Spider-Man, Iron Man, Captain America, etc.)
- Teams (Avengers, X-Men)
- Events (Infinity Gauntlet, Civil War)

### Step 2: Download Images

1. Run the image setup script:
   ```bash
   python scripts/2_fetch_marvel_images.py
   ```

2. Download Marvel images from:
   - Marvel official website
   - Marvel Wiki (marvel.fandom.com)
   - Comic book databases
   - Official promotional materials

3. Place images in `raw_data/images/` directory

### Step 3: Download Audio

1. Run the audio setup script:
   ```bash
   python scripts/3_fetch_marvel_audio.py
   ```

2. Download Marvel audio from:
   - YouTube (using yt-dlp)
   - Podcast platforms
   - Official Marvel channels

3. Place audio files in `raw_data/audio/` directory

### Step 4: Process Content

Process all content and create the vector database:

```bash
python scripts/4_process_marvel_content.py
```

This will:
- Process documents into chunks
- Process images (generate descriptions)
- Create vector embeddings
- Store in ChromaDB

### Step 5: Query the Database

Query the Marvel knowledge base:

```bash
python scripts/5_marvel_rag_query.py
```

Example queries:
- "Tell me about Spider-Man's powers"
- "What is the Infinity Gauntlet?"
- "Who are the founding members of the Avengers?"
- "Describe the Civil War event"

## 🔧 Configuration

### Models

The system uses:
- **Embeddings**: `BAAI/bge-large-en-v1.5` (HuggingFace)
- **LLM**: `mistral:7b` (via Ollama)

### Vector Database

- **Database**: ChromaDB
- **Collection**: `marvel_knowledge_base`
- **Location**: `vectorstore/` directory

## 📊 Data Sources

### Documents
- Marvel character bios
- Team information
- Event descriptions
- Storyline summaries

### Images
- Character artwork
- Comic book covers
- Team lineups
- Concept art

### Audio
- Character origin stories
- Comic book discussions
- Movie interviews
- Podcasts about Marvel

## 🎯 Usage Examples

### Query Characters
```
Question: What are Spider-Man's powers?
Answer: [Retrieved from vector database with context about Spider-Man]
```

### Query Storylines
```
Question: Tell me about the Civil War event
Answer: [Retrieved information about Civil War with character details]
```

### Query Teams
```
Question: Who are the founding members of the Avengers?
Answer: [List of founding members with details]
```

## 🔍 Integration with Marvel RAG Notebook

This vector database can be integrated with the `multimodal_rag_final_marvel.ipynb` notebook:

1. Process content using this pipeline
2. Export the vectorstore
3. Load in the notebook for enhanced RAG capabilities

## 📝 Notes

- **Copyright**: Ensure you have rights to download and use content
- **Rate Limiting**: Be respectful when downloading from web sources
- **Storage**: Vector database can be large; ensure sufficient disk space
- **GPU**: Optional but recommended for faster processing

## 🐛 Troubleshooting

### Ollama not running
```bash
# Start Ollama
ollama serve

# Check status
curl http://localhost:11434/
```

### Vector database not found
```bash
# Make sure you've run the processing script
python scripts/4_process_marvel_content.py
```

### Images not processing
- Check image file formats (jpg, png, etc.)
- Ensure images are in `raw_data/images/` directory
- Check file permissions

### Audio not processing
- Install Whisper for transcription
- Check audio file formats (mp3, wav, etc.)
- Use the notebook for advanced audio processing

## 📚 Additional Resources

- [Marvel Official Website](https://www.marvel.com/)
- [Marvel Wiki](https://marvel.fandom.com/)
- [Ollama Documentation](https://ollama.com/)
- [ChromaDB Documentation](https://www.trychroma.com/)

## 🤝 Contributing

Feel free to add more Marvel content sources or improve the processing pipeline!

## 📄 License

This project is for educational purposes. Respect copyright when downloading content.

