"""
Main pipeline script to build Marvel vector database
Run this script to execute the complete pipeline
"""
import os
import sys
from pathlib import Path

def run_script(script_name, description):
    """Run a script and handle errors"""
    print(f"\n{'='*60}")
    print(f"📋 {description}")
    print(f"{'='*60}")
    
    script_path = Path(__file__).parent / script_name
    
    if not script_path.exists():
        print(f"❌ Script not found: {script_path}")
        return False
    
    try:
        # Change to script directory
        os.chdir(script_path.parent)
        
        # Import and run script
        if script_name.endswith('.py'):
            module_name = script_name[:-3]
            module = __import__(f'scripts.{module_name}', fromlist=[module_name])
            
            if hasattr(module, 'main'):
                module.main()
                return True
            else:
                print(f"❌ Script {script_name} doesn't have a main() function")
                return False
        else:
            print(f"❌ Invalid script: {script_name}")
            return False
            
    except Exception as e:
        print(f"❌ Error running {script_name}: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main pipeline execution"""
    print("🦸 Marvel Vector Database Pipeline")
    print("=" * 60)
    print("\nThis pipeline will:")
    print("1. Fetch Marvel documents from web")
    print("2. Set up image and audio fetching")
    print("3. Process all content into vector embeddings")
    print("4. Create vector database")
    print("\nLet's begin!\n")
    
    # Step 1: Fetch documents
    print("\n" + "="*60)
    print("STEP 1: Fetching Marvel Documents")
    print("="*60)
    run_script("1_fetch_marvel_documents.py", "Fetching Marvel Documents")
    
    # Step 2: Set up image fetching
    print("\n" + "="*60)
    print("STEP 2: Setting up Image Fetching")
    print("="*60)
    run_script("2_fetch_marvel_images.py", "Setting up Image Fetching")
    
    # Step 3: Set up audio fetching
    print("\n" + "="*60)
    print("STEP 3: Setting up Audio Fetching")
    print("="*60)
    run_script("3_fetch_marvel_audio.py", "Setting up Audio Fetching")
    
    # Step 4: Process content
    print("\n" + "="*60)
    print("STEP 4: Processing Content and Creating Vector Database")
    print("="*60)
    print("\n⚠️  Note: Make sure you've downloaded images and audio files")
    print("   before running the processing step.")
    
    response = input("\n   Continue with processing? (y/n): ")
    if response.lower() == 'y':
        run_script("4_process_marvel_content.py", "Processing Content")
    
    print("\n" + "="*60)
    print("✅ Pipeline Complete!")
    print("="*60)
    print("\nNext steps:")
    print("1. Download images and audio files (see instructions in raw_data folders)")
    print("2. Run processing again: python 4_process_marvel_content.py")
    print("3. Query the database: python 5_marvel_rag_query.py")
    print("\n" + "="*60)

if __name__ == "__main__":
    # Change to scripts directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir.parent)
    
    main()

