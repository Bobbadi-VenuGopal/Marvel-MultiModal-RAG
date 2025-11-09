"""
Fetch Marvel audio content (podcasts, interviews, etc.)
"""
import os
import json
import time
from pathlib import Path
import yt_dlp
import requests

class MarvelAudioFetcher:
    def __init__(self, output_dir=None):
        if output_dir is None:
            script_dir = Path(__file__).parent.parent
            output_dir = script_dir / "raw_data" / "audio"
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def download_youtube_audio(self, url, output_filename=None):
        """Download audio from YouTube URL"""
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': str(self.output_dir / (output_filename or '%(title)s.%(ext)s')),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'quiet': False,
                'no_warnings': False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return True
        except Exception as e:
            print(f"Error downloading YouTube audio: {e}")
            return False
    
    def create_marvel_audio_sources(self):
        """Create a list of Marvel audio sources"""
        audio_sources = {
            "podcasts": [
                {
                    "name": "Marvel Cinematic Universe Podcast",
                    "description": "Discussion about MCU movies and characters",
                    "url": "https://www.youtube.com/watch?v=EXAMPLE",  # Placeholder
                    "type": "podcast"
                },
                {
                    "name": "Marvel Comics History",
                    "description": "History of Marvel Comics and characters",
                    "url": "https://www.youtube.com/watch?v=EXAMPLE",  # Placeholder
                    "type": "podcast"
                }
            ],
            "interviews": [
                {
                    "name": "Stan Lee Interview",
                    "description": "Interview with Stan Lee about creating Marvel characters",
                    "url": "https://www.youtube.com/watch?v=EXAMPLE",  # Placeholder
                    "type": "interview"
                },
                {
                    "name": "Marvel Writers Roundtable",
                    "description": "Discussion with Marvel comic book writers",
                    "url": "https://www.youtube.com/watch?v=EXAMPLE",  # Placeholder
                    "type": "interview"
                }
            ],
            "audiobooks": [
                {
                    "name": "Marvel Comics Origin Stories",
                    "description": "Audiobook about Marvel character origins",
                    "url": "https://example.com/audiobook.mp3",  # Placeholder
                    "type": "audiobook"
                }
            ]
        }
        
        return audio_sources
    
    def save_audio_metadata(self, audio_sources):
        """Save audio metadata to JSON file"""
        metadata = {
            'total_audio': sum(len(audios) for audios in audio_sources.values()),
            'categories': audio_sources,
            'created_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'note': 'Replace placeholder URLs with actual audio sources'
        }
        
        metadata_path = self.output_dir / 'audio_metadata.json'
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"📄 Audio metadata saved to {metadata_path}")
        return str(metadata_path)
    
    def create_instruction_file(self):
        """Create instructions for downloading Marvel audio"""
        instructions = """
# Marvel Audio Download Instructions

## Sources for Marvel Audio

1. **YouTube**
   - Marvel official channel videos
   - Comic book discussion podcasts
   - Character origin story videos
   - Movie interviews and behind-the-scenes

2. **Podcasts**
   - Marvel Cinematic Universe podcasts
   - Comic book history podcasts
   - Character analysis podcasts

3. **Audiobooks**
   - Marvel Comics audiobooks
   - Character origin story audiobooks
   - Graphic novel audiobooks

4. **Interviews**
   - Stan Lee interviews
   - Marvel writers and artists interviews
   - Actor interviews about Marvel characters

## Download Methods

### YouTube (using yt-dlp)
```bash
pip install yt-dlp
python 3_fetch_marvel_audio.py --youtube-url <URL>
```

### Direct Download
- Download MP3 files directly from sources
- Place in raw_data/audio directory

## File Naming Convention

- Podcasts: `podcast_[name].mp3`
- Interviews: `interview_[name].mp3`
- Audiobooks: `audiobook_[name].mp3`

## Processing

After downloading audio, run the processing script to:
1. Transcribe audio to text
2. Generate embeddings
3. Store in vector database

## Legal Note

Ensure you have the right to download and use the audio content.
Respect copyright and terms of service.
        """.strip()
        
        instruction_path = self.output_dir / 'DOWNLOAD_INSTRUCTIONS.md'
        with open(instruction_path, 'w', encoding='utf-8') as f:
            f.write(instructions)
        
        print(f"📄 Instructions saved to {instruction_path}")

def main():
    """Main function to set up Marvel audio fetching"""
    print("🎵 Starting Marvel Audio Fetching Setup...")
    
    fetcher = MarvelAudioFetcher()
    
    # Create audio sources list
    print("\n📋 Creating audio sources list...")
    audio_sources = fetcher.create_marvel_audio_sources()
    
    # Save metadata
    metadata_path = fetcher.save_audio_metadata(audio_sources)
    
    # Create instructions
    fetcher.create_instruction_file()
    
    print(f"\n✅ Audio fetching setup complete!")
    print(f"📝 Total audio references: {sum(len(audios) for audios in audio_sources.values())}")
    print(f"⚠️  Note: Replace placeholder URLs with actual audio URLs")
    print(f"📖 See DOWNLOAD_INSTRUCTIONS.md for more information")
    print(f"\n💡 To download from YouTube, install yt-dlp:")
    print(f"   pip install yt-dlp")

if __name__ == "__main__":
    main()

