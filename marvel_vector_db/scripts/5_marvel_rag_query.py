"""
Marvel RAG Query Interface
Query the Marvel vector database using RAG
"""
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain.storage import InMemoryStore
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM
import torch
import requests

class MarvelRAGQuery:
    def __init__(self, vectorstore_dir=None):
        if vectorstore_dir is None:
            script_dir = Path(__file__).parent.parent
            vectorstore_dir = script_dir / "vectorstore"
        self.vectorstore_dir = Path(vectorstore_dir)
        
        print("🔧 Initializing Marvel RAG Query System...")
        
        # Initialize embeddings
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-large-en-v1.5",
            model_kwargs={"device": device},
            encode_kwargs={"normalize_embeddings": True}
        )
        
        # Load vectorstore
        try:
            self.vectorstore = Chroma(
                collection_name="marvel_knowledge_base",
                embedding_function=self.embeddings,
                persist_directory=str(self.vectorstore_dir)
            )
            print("   ✅ Vectorstore loaded")
        except Exception as e:
            print(f"   ❌ Error loading vectorstore: {e}")
            raise
        
        # Initialize LLM
        try:
            self.llm = OllamaLLM(model="mistral:7b", temperature=0.1)
            print("   ✅ LLM initialized")
        except Exception as e:
            print(f"   ⚠️  LLM not available: {e}")
            self.llm = None
        
        # Create retriever
        self.doc_store = InMemoryStore()
        self.retriever = MultiVectorRetriever(
            vectorstore=self.vectorstore,
            docstore=self.doc_store,
            id_key="doc_id"
        )
    
    def query(self, question, k=5):
        """Query the Marvel knowledge base"""
        print(f"\n🔍 Querying: {question}")
        print(f"   Retrieving top {k} relevant documents...")
        
        # Retrieve relevant documents
        try:
            docs = self.retriever.get_relevant_documents(question, k=k)
            print(f"   ✅ Found {len(docs)} relevant documents")
        except Exception as e:
            print(f"   ❌ Error retrieving documents: {e}")
            return None
        
        # Combine context
        context = "\n\n".join([doc.page_content for doc in docs])
        
        # Generate response using LLM
        if self.llm:
            prompt = f"""You are a Marvel Comics expert assistant. Answer the following question about Marvel characters, storylines, comics, or universe based on the provided context.

Context from Marvel knowledge base:
{context[:2000]}

Question: {question}

Please provide a comprehensive answer focusing on:
- Specific character names, powers, and storylines
- Marvel universe details and events
- Comic book history and notable storylines
- Team affiliations and relationships

Answer:"""
            
            try:
                response = self.llm.invoke(prompt)
                return {
                    'question': question,
                    'answer': response,
                    'sources': [doc.metadata for doc in docs],
                    'num_sources': len(docs)
                }
            except Exception as e:
                print(f"   ❌ Error generating response: {e}")
                return {
                    'question': question,
                    'answer': "I found relevant information but couldn't generate a response. Please check if Ollama is running.",
                    'sources': [doc.metadata for doc in docs],
                    'num_sources': len(docs),
                    'context': context[:1000]
                }
        else:
            # Return context without LLM processing
            return {
                'question': question,
                'answer': "LLM not available. Here's the relevant context:",
                'context': context[:2000],
                'sources': [doc.metadata for doc in docs],
                'num_sources': len(docs)
            }
    
    def interactive_query(self):
        """Interactive query interface"""
        print("\n" + "=" * 60)
        print("🦸 Marvel RAG Query Interface")
        print("=" * 60)
        print("\nAsk questions about Marvel characters, storylines, comics, or universe.")
        print("Type 'quit' or 'exit' to stop.\n")
        
        while True:
            question = input("❓ Your question: ").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if not question:
                continue
            
            result = self.query(question)
            
            if result:
                print("\n" + "-" * 60)
                print("📖 Answer:")
                print(result['answer'])
                print(f"\n📚 Sources: {result['num_sources']} documents found")
                if result.get('sources'):
                    print("   Sources:")
                    for i, source in enumerate(result['sources'][:3], 1):
                        source_name = source.get('source', 'Unknown')
                        source_type = source.get('type', 'unknown')
                        print(f"   {i}. {source_name} ({source_type})")
                print("-" * 60 + "\n")

def check_ollama():
    """Check if Ollama is running"""
    try:
        response = requests.get("http://localhost:11434/", timeout=3)
        return response.status_code == 200
    except:
        return False

def main():
    """Main function"""
    # Check Ollama
    if not check_ollama():
        print("⚠️  Warning: Ollama is not running.")
        print("   Install and start Ollama for LLM responses:")
        print("   1. Install: https://ollama.com/")
        print("   2. Start: ollama serve")
        print("   3. Pull model: ollama pull mistral:7b")
        print("\n   You can still query the vector database, but responses will be limited.")
        response = input("\n   Continue anyway? (y/n): ")
        if response.lower() != 'y':
            return
    
    # Initialize RAG system
    try:
        rag = MarvelRAGQuery()
    except Exception as e:
        print(f"\n❌ Error initializing RAG system: {e}")
        print("   Make sure you've run the processing script first:")
        print("   python 4_process_marvel_content.py")
        return
    
    # Start interactive query
    rag.interactive_query()

if __name__ == "__main__":
    main()

