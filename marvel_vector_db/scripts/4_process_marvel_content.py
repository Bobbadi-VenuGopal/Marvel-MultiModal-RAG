"""
Process Marvel content and create vector database
"""
import os
import sys
import json
import pickle
import base64
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain.schema.document import Document
from langchain.storage import InMemoryStore
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM
import torch
from unstructured.partition.pdf import partition_pdf
from PIL import Image
import io

class MarvelContentProcessor:
    def __init__(self, 
                 raw_data_dir=None,
                 processed_data_dir=None,
                 vectorstore_dir=None):
        script_dir = Path(__file__).parent.parent
        self.raw_data_dir = Path(raw_data_dir) if raw_data_dir else script_dir / "raw_data"
        self.processed_data_dir = Path(processed_data_dir) if processed_data_dir else script_dir / "processed_data"
        self.vectorstore_dir = Path(vectorstore_dir) if vectorstore_dir else script_dir / "vectorstore"
        
        # Create directories
        self.processed_data_dir.mkdir(parents=True, exist_ok=True)
        self.vectorstore_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize models
        print("🔧 Initializing models...")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"   Using device: {device}")
        
        self.embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-large-en-v1.5",
            model_kwargs={"device": device},
            encode_kwargs={"normalize_embeddings": True}
        )
        
        # Initialize LLM for summarization
        try:
            self.llm = OllamaLLM(model="mistral:7b", temperature=0.1)
            print("   ✅ LLM initialized")
        except Exception as e:
            print(f"   ⚠️  LLM not available: {e}")
            self.llm = None
        
        # Initialize vectorstore
        self.vectorstore = Chroma(
            collection_name="marvel_knowledge_base",
            embedding_function=self.embeddings,
            persist_directory=str(self.vectorstore_dir)
        )
        
        self.doc_store = InMemoryStore()
        self.processed_count = {
            'documents': 0,
            'images': 0,
            'audio': 0
        }
    
    def process_documents(self):
        """Process Marvel documents"""
        print("\n📄 Processing documents...")
        documents_dir = self.raw_data_dir / "documents"
        
        if not documents_dir.exists():
            print("   ⚠️  Documents directory not found")
            return
        
        text_files = list(documents_dir.glob("*.txt"))
        print(f"   Found {len(text_files)} text files")
        
        all_documents = []
        
        for text_file in text_files:
            try:
                print(f"   Processing {text_file.name}...")
                
                with open(text_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Split into chunks
                chunks = self._split_text_into_chunks(content, chunk_size=1000)
                
                for i, chunk in enumerate(chunks):
                    doc = Document(
                        page_content=chunk,
                        metadata={
                            'source': str(text_file.name),
                            'chunk_id': i,
                            'type': 'document',
                            'category': self._extract_category(text_file.name)
                        }
                    )
                    all_documents.append(doc)
                
                self.processed_count['documents'] += 1
                print(f"      ✅ Processed into {len(chunks)} chunks")
                
            except Exception as e:
                print(f"      ❌ Error processing {text_file.name}: {e}")
        
        # Add to vectorstore
        if all_documents:
            print(f"   📤 Adding {len(all_documents)} document chunks to vectorstore...")
            self.vectorstore.add_documents(all_documents)
            print(f"   ✅ Documents added to vectorstore")
    
    def process_images(self):
        """Process Marvel images"""
        print("\n🖼️  Processing images...")
        images_dir = self.raw_data_dir / "images"
        
        if not images_dir.exists():
            print("   ⚠️  Images directory not found")
            return
        
        # Get image files
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        image_files = []
        for ext in image_extensions:
            image_files.extend(list(images_dir.glob(f"*{ext}")))
            image_files.extend(list(images_dir.glob(f"*{ext.upper()}")))
        
        print(f"   Found {len(image_files)} image files")
        
        if not image_files:
            print("   ⚠️  No images found. Please download images first.")
            return
        
        all_image_docs = []
        
        for image_file in image_files:
            try:
                print(f"   Processing {image_file.name}...")
                
                # Load image
                with open(image_file, 'rb') as f:
                    image_data = f.read()
                
                # Convert to base64
                image_b64 = base64.b64encode(image_data).decode('utf-8')
                
                # Create description (if LLM available, could generate description)
                description = self._generate_image_description(image_file.name)
                
                doc = Document(
                    page_content=description,
                    metadata={
                        'source': str(image_file.name),
                        'type': 'image',
                        'image_b64': image_b64,
                        'category': self._extract_category(image_file.name)
                    }
                )
                all_image_docs.append(doc)
                
                self.processed_count['images'] += 1
                print(f"      ✅ Processed")
                
            except Exception as e:
                print(f"      ❌ Error processing {image_file.name}: {e}")
        
        # Add to vectorstore
        if all_image_docs:
            print(f"   📤 Adding {len(all_image_docs)} images to vectorstore...")
            self.vectorstore.add_documents(all_image_docs)
            print(f"   ✅ Images added to vectorstore")
    
    def process_audio(self):
        """Process Marvel audio files"""
        print("\n🎵 Processing audio files...")
        audio_dir = self.raw_data_dir / "audio"
        
        if not audio_dir.exists():
            print("   ⚠️  Audio directory not found")
            return
        
        # Get audio files
        audio_extensions = ['.mp3', '.wav', '.m4a', '.flac']
        audio_files = []
        for ext in audio_extensions:
            audio_files.extend(list(audio_dir.glob(f"*{ext}")))
            audio_files.extend(list(audio_dir.glob(f"*{ext.upper()}")))
        
        print(f"   Found {len(audio_files)} audio files")
        
        if not audio_files:
            print("   ⚠️  No audio files found. Please download audio first.")
            return
        
        # Note: Audio transcription requires Whisper or similar
        # For now, we'll create placeholders
        print("   ⚠️  Audio transcription not implemented in this script.")
        print("   💡 Use the multimodal_rag_final_marvel.ipynb notebook for audio processing.")
    
    def _split_text_into_chunks(self, text, chunk_size=1000, overlap=200):
        """Split text into overlapping chunks"""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start = end - overlap
        
        return chunks
    
    def _extract_category(self, filename):
        """Extract category from filename"""
        filename_lower = filename.lower()
        if 'character' in filename_lower:
            return 'character'
        elif 'team' in filename_lower:
            return 'team'
        elif 'event' in filename_lower:
            return 'event'
        elif 'comic' in filename_lower:
            return 'comic'
        else:
            return 'general'
    
    def _generate_image_description(self, filename):
        """Generate description for image"""
        # Simple description based on filename
        # In production, use vision model to generate descriptions
        name = Path(filename).stem.replace('_', ' ').title()
        return f"Marvel image: {name}. This image likely contains Marvel Comics content such as characters, comic book covers, or team lineups."
    
    def create_retriever(self):
        """Create retriever from vectorstore"""
        retriever = MultiVectorRetriever(
            vectorstore=self.vectorstore,
            docstore=self.doc_store,
            id_key="doc_id"
        )
        return retriever
    
    def save_metadata(self):
        """Save processing metadata"""
        metadata = {
            'processed_at': datetime.now().isoformat(),
            'processed_count': self.processed_count,
            'vectorstore_path': str(self.vectorstore_dir),
            'total_documents': self.vectorstore._collection.count() if hasattr(self.vectorstore, '_collection') else 0
        }
        
        metadata_path = self.processed_data_dir / 'processing_metadata.json'
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"\n📄 Metadata saved to {metadata_path}")
        return metadata

def main():
    """Main processing function"""
    print("🦸 Marvel Content Processing Pipeline")
    print("=" * 50)
    
    processor = MarvelContentProcessor()
    
    # Process all content types
    processor.process_documents()
    processor.process_images()
    processor.process_audio()
    
    # Create retriever
    retriever = processor.create_retriever()
    
    # Save metadata
    metadata = processor.save_metadata()
    
    print("\n" + "=" * 50)
    print("✅ Processing complete!")
    print(f"📊 Processed:")
    print(f"   Documents: {processor.processed_count['documents']}")
    print(f"   Images: {processor.processed_count['images']}")
    print(f"   Audio: {processor.processed_count['audio']}")
    print(f"\n💾 Vector database saved to: {processor.vectorstore_dir}")
    print(f"📈 Total documents in vectorstore: {metadata.get('total_documents', 0)}")

if __name__ == "__main__":
    main()

