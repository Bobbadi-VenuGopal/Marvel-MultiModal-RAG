"""
Fetch Marvel images from web sources
"""
import requests
import os
import json
import time
from urllib.parse import urlparse
from pathlib import Path
import base64
from PIL import Image
import io

class MarvelImageFetcher:
    def __init__(self, output_dir=None):
        if output_dir is None:
            script_dir = Path(__file__).parent.parent
            output_dir = script_dir / "raw_data" / "images"
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.downloaded_images = []
    
    def download_image(self, url, filename):
        """Download an image from URL"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10, stream=True)
            if response.status_code == 200:
                filepath = self.output_dir / filename
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                return str(filepath)
            return None
        except Exception as e:
            print(f"Error downloading image {url}: {e}")
            return None
    
    def create_sample_images_list(self):
        """Create a list of Marvel image URLs to download"""
        # Note: In production, you would use actual image URLs from Marvel APIs or websites
        # For now, we'll create placeholder references that users can replace
        
        image_sources = {
            "characters": [
                {
                    "name": "Spider-Man",
                    "description": "Classic Spider-Man character image",
                    "url": "https://example.com/spiderman.jpg",  # Placeholder
                    "type": "character"
                },
                {
                    "name": "Iron Man",
                    "description": "Iron Man in armor",
                    "url": "https://example.com/ironman.jpg",  # Placeholder
                    "type": "character"
                },
                {
                    "name": "Captain America",
                    "description": "Captain America with shield",
                    "url": "https://example.com/captainamerica.jpg",  # Placeholder
                    "type": "character"
                },
                {
                    "name": "Thor",
                    "description": "Thor with Mjolnir",
                    "url": "https://example.com/thor.jpg",  # Placeholder
                    "type": "character"
                },
                {
                    "name": "Hulk",
                    "description": "The Incredible Hulk",
                    "url": "https://example.com/hulk.jpg",  # Placeholder
                    "type": "character"
                }
            ],
            "comics": [
                {
                    "name": "Avengers #1",
                    "description": "First Avengers comic cover",
                    "url": "https://example.com/avengers1.jpg",  # Placeholder
                    "type": "comic_cover"
                },
                {
                    "name": "Amazing Spider-Man #1",
                    "description": "First Amazing Spider-Man comic cover",
                    "url": "https://example.com/asm1.jpg",  # Placeholder
                    "type": "comic_cover"
                }
            ],
            "teams": [
                {
                    "name": "The Avengers",
                    "description": "Avengers team lineup",
                    "url": "https://example.com/avengers_team.jpg",  # Placeholder
                    "type": "team"
                },
                {
                    "name": "X-Men",
                    "description": "X-Men team lineup",
                    "url": "https://example.com/xmen_team.jpg",  # Placeholder
                    "type": "team"
                }
            ]
        }
        
        return image_sources
    
    def save_image_metadata(self, image_sources):
        """Save image metadata to JSON file"""
        metadata = {
            'total_images': sum(len(images) for images in image_sources.values()),
            'categories': image_sources,
            'created_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'note': 'Replace placeholder URLs with actual image URLs from Marvel sources'
        }
        
        metadata_path = self.output_dir / 'image_metadata.json'
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"📄 Image metadata saved to {metadata_path}")
        return str(metadata_path)
    
    def download_from_list(self, image_list, delay=1):
        """Download images from a list of URLs"""
        downloaded = []
        
        for img_info in image_list:
            url = img_info.get('url', '')
            name = img_info.get('name', 'unknown')
            
            # Skip placeholder URLs
            if 'example.com' in url:
                print(f"⚠️  Skipping placeholder URL for {name}")
                continue
            
            print(f"📥 Downloading {name}...")
            filename = f"{name.replace(' ', '_')}.jpg"
            filepath = self.download_image(url, filename)
            
            if filepath:
                downloaded.append({
                    **img_info,
                    'filepath': filepath,
                    'downloaded': True
                })
                print(f"  ✅ Saved to {filepath}")
            else:
                print(f"  ❌ Failed to download {name}")
            
            time.sleep(delay)  # Be polite to servers
        
        return downloaded
    
    def create_instruction_file(self):
        """Create instructions for downloading Marvel images"""
        instructions = """
# Marvel Image Download Instructions

## Sources for Marvel Images

1. **Marvel Official Website**
   - Visit https://www.marvel.com/characters
   - Download character images and artwork

2. **Marvel Comics Database**
   - Visit https://marvel.fandom.com/
   - Browse character pages and download images

3. **Marvel API** (if available)
   - Check https://developer.marvel.com/
   - Use API to fetch character images

4. **Comic Book Covers**
   - Visit comic book databases
   - Download cover artwork

5. **Fan Art and Official Artwork**
   - Use official Marvel promotional materials
   - Respect copyright when downloading

## Image Types to Collect

- Character portraits
- Comic book covers
- Team lineups
- Action scenes
- Concept art
- Movie stills (if applicable)

## File Naming Convention

- Characters: `character_[name].jpg`
- Comics: `comic_[series]_[issue].jpg`
- Teams: `team_[name].jpg`
- Events: `event_[name].jpg`

## Processing

After downloading images, run the processing script to:
1. Convert to consistent format
2. Generate embeddings
3. Store in vector database
        """.strip()
        
        instruction_path = self.output_dir / 'DOWNLOAD_INSTRUCTIONS.md'
        with open(instruction_path, 'w', encoding='utf-8') as f:
            f.write(instructions)
        
        print(f"📄 Instructions saved to {instruction_path}")

def main():
    """Main function to set up Marvel image fetching"""
    print("🖼️  Starting Marvel Image Fetching Setup...")
    
    fetcher = MarvelImageFetcher()
    
    # Create image sources list
    print("\n📋 Creating image sources list...")
    image_sources = fetcher.create_sample_images_list()
    
    # Save metadata
    metadata_path = fetcher.save_image_metadata(image_sources)
    
    # Create instructions
    fetcher.create_instruction_file()
    
    print(f"\n✅ Image fetching setup complete!")
    print(f"📝 Total image references: {sum(len(images) for images in image_sources.values())}")
    print(f"⚠️  Note: Replace placeholder URLs with actual image URLs")
    print(f"📖 See DOWNLOAD_INSTRUCTIONS.md for more information")

if __name__ == "__main__":
    main()

