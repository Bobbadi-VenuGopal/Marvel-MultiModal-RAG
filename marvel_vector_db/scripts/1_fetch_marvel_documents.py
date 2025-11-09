"""
Fetch Marvel documents from web sources (Wikipedia, Marvel Wiki, etc.)
"""
import requests
from bs4 import BeautifulSoup
import os
import json
import time
from urllib.parse import urljoin, urlparse
from pathlib import Path
import re

class MarvelDocumentFetcher:
    def __init__(self, output_dir=None):
        if output_dir is None:
            # Get the script directory and navigate to raw_data/documents
            script_dir = Path(__file__).parent.parent
            output_dir = script_dir / "raw_data" / "documents"
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
    def fetch_wikipedia_page(self, title, lang='en'):
        """Fetch a Wikipedia page"""
        try:
            url = f"https://{lang}.wikipedia.org/api/rest_v1/page/html/{title}"
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                return response.text
            return None
        except Exception as e:
            print(f"Error fetching Wikipedia page {title}: {e}")
            return None
    
    def fetch_wikipedia_text(self, title, lang='en'):
        """Fetch Wikipedia page as plain text"""
        try:
            url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{title}"
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                content = f"{data.get('title', '')}\n\n{data.get('extract', '')}"
                return content
            return None
        except Exception as e:
            print(f"Error fetching Wikipedia text {title}: {e}")
            return None
    
    def fetch_marvel_characters(self, character_list):
        """Fetch information about Marvel characters"""
        characters_data = []
        
        for character in character_list:
            print(f"Fetching data for {character}...")
            
            # Try Wikipedia
            wiki_title = character.replace(' ', '_')
            content = self.fetch_wikipedia_text(wiki_title)
            
            if content:
                # Save to file
                filename = re.sub(r'[^\w\s-]', '', character).strip().replace(' ', '_')
                filepath = self.output_dir / f"{filename}_wikipedia.txt"
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                characters_data.append({
                    'character': character,
                    'source': 'wikipedia',
                    'file': str(filepath),
                    'content_length': len(content)
                })
                print(f"  Saved {len(content)} characters to {filepath}")
            else:
                print(f"  Could not fetch data for {character}")
            
            time.sleep(1)  # Be polite to servers
        
        return characters_data
    
    def create_marvel_wiki_content(self):
        """Create Marvel content from known information"""
        marvel_content = {
            "characters": [
                {
                    "name": "Spider-Man",
                    "content": """
Spider-Man (Peter Parker) is a superhero appearing in American comic books published by Marvel Comics. 
Created by writer-editor Stan Lee and artist Steve Ditko, he first appeared in Amazing Fantasy #15 (August 1962).

Powers and Abilities:
- Superhuman strength, speed, agility, reflexes, and durability
- Ability to cling to most surfaces
- Precognitive "spider-sense" that alerts him to danger
- Genius-level intellect
- Proficient scientist and inventor
- Master of hand-to-hand combat

Notable Storylines:
- The Death of Gwen Stacy
- The Clone Saga
- Civil War
- One More Day
- Superior Spider-Man
                    """.strip()
                },
                {
                    "name": "Iron Man",
                    "content": """
Iron Man (Anthony Edward "Tony" Stark) is a superhero appearing in American comic books published by Marvel Comics.
Created by writer and editor Stan Lee, developed by scripter Larry Lieber, and designed by artists Don Heck and Jack Kirby,
he first appeared in Tales of Suspense #39 (March 1963).

Powers and Abilities:
- Genius-level intellect
- Expert engineer and inventor
- Proficient in multiple fields of science
- Advanced powered armor suit
- Flight capabilities
- Energy repulsors and various weapons systems
- Extremis virus enhancement (in some storylines)

Notable Storylines:
- Demon in a Bottle
- Armor Wars
- Extremis
- Civil War
- The Invincible Iron Man
                    """.strip()
                },
                {
                    "name": "Captain America",
                    "content": """
Captain America (Steven Grant "Steve" Rogers) is a superhero appearing in American comic books published by Marvel Comics.
Created by cartoonists Joe Simon and Jack Kirby, he first appeared in Captain America Comics #1 (March 1941).

Powers and Abilities:
- Peak human physical condition
- Enhanced strength, speed, agility, durability, and reflexes
- Master martial artist and hand-to-hand combatant
- Expert tactician and strategist
- Wields vibranium shield
- Slowed aging process

Notable Storylines:
- The Death of Captain America
- Civil War
- Secret Empire
- The Winter Soldier
- Captain America: Reborn
                    """.strip()
                },
                {
                    "name": "Thor",
                    "content": """
Thor Odinson is a superhero appearing in American comic books published by Marvel Comics.
Based on the Norse mythological deity of the same name, the character was created by Stan Lee, Larry Lieber, and Jack Kirby,
first appearing in Journey into Mystery #83 (August 1962).

Powers and Abilities:
- Superhuman strength, speed, agility, durability, and longevity
- Weather manipulation
- Flight via Mjolnir
- Control over lightning and thunder
- Dimensional travel via Bifrost
- Asgardian physiology

Notable Storylines:
- The Death of Thor
- Ragnarok
- Fear Itself
- The Unworthy Thor
- War of the Realms
                    """.strip()
                },
                {
                    "name": "Hulk",
                    "content": """
The Hulk (Robert Bruce Banner) is a superhero appearing in American comic books published by Marvel Comics.
Created by writer Stan Lee and artist Jack Kirby, he first appeared in The Incredible Hulk #1 (May 1962).

Powers and Abilities:
- Superhuman strength that increases with anger
- Accelerated healing factor
- Near invulnerability
- Enhanced durability and endurance
- Genius-level intellect (as Banner)
- Multiple personalities and transformations

Notable Storylines:
- Planet Hulk
- World War Hulk
- The Immortal Hulk
- World War Hulk
- Future Imperfect
                    """.strip()
                },
                {
                    "name": "Black Widow",
                    "content": """
Black Widow (Natasha Romanoff) is a superhero appearing in American comic books published by Marvel Comics.
Created by editor and plotter Stan Lee, scripter Don Rico, and artist Don Heck, she first appeared in Tales of Suspense #52 (April 1964).

Powers and Abilities:
- Peak human physical condition
- Master martial artist and hand-to-hand combatant
- Expert marksman and weapons specialist
- Espionage and infiltration expert
- Slowed aging (enhanced by Red Room)
- Widow's Bite (electroshock weapons)

Notable Storylines:
- The Name of the Rose
- Black Widow: Deadly Origin
- Black Widow: The Itsy-Bitsy Spider
- Black Widow (2020 series)
                    """.strip()
                },
                {
                    "name": "Doctor Strange",
                    "content": """
Doctor Strange (Stephen Vincent Strange) is a superhero appearing in American comic books published by Marvel Comics.
Created by artist Steve Ditko and writer Stan Lee, he first appeared in Strange Tales #110 (July 1963).

Powers and Abilities:
- Master of the mystic arts
- Reality manipulation
- Dimensional travel
- Astral projection
- Energy manipulation
- Time manipulation (via Eye of Agamotto)
- Various mystical artifacts (Cloak of Levitation, Eye of Agamotto)

Notable Storylines:
- The Oath
- Triumph and Torment
- The Death of Doctor Strange
- Damnation
- Strange (2023 series)
                    """.strip()
                },
                {
                    "name": "Wolverine",
                    "content": """
Wolverine (James "Logan" Howlett) is a superhero appearing in American comic books published by Marvel Comics.
Created by writer Len Wein and artist John Romita Sr., he first appeared in The Incredible Hulk #180 (October 1974).

Powers and Abilities:
- Enhanced senses
- Regenerative healing factor
- Retractable adamantium claws
- Superhuman strength, speed, agility, and reflexes
- Extended longevity
- Master martial artist
- Expert tracker

Notable Storylines:
- Weapon X
- Old Man Logan
- The Death of Wolverine
- Return of Wolverine
- House of X / Powers of X
                    """.strip()
                }
            ],
            "teams": [
                {
                    "name": "Avengers",
                    "content": """
The Avengers are a team of superheroes appearing in American comic books published by Marvel Comics.
Created by writer-editor Stan Lee and artist/co-plotter Jack Kirby, the team first appeared in The Avengers #1 (September 1963).

Founding Members:
- Iron Man
- Thor
- Hulk
- Ant-Man
- Wasp
- Captain America (joined shortly after)

Notable Storylines:
- The Kree-Skrull War
- Avengers Disassembled
- Civil War
- Secret Invasion
- Siege
- Infinity
- Secret Wars (2015)
                    """.strip()
                },
                {
                    "name": "X-Men",
                    "content": """
The X-Men are a team of superheroes appearing in American comic books published by Marvel Comics.
Created by writer-editor Stan Lee and artist/co-plotter Jack Kirby, the team first appeared in The X-Men #1 (September 1963).

Founding Members:
- Professor X
- Cyclops
- Marvel Girl (Jean Grey)
- Beast
- Iceman
- Angel

Notable Storylines:
- Dark Phoenix Saga
- Days of Future Past
- Age of Apocalypse
- House of M
- Messiah Complex
- House of X / Powers of X
                    """.strip()
                }
            ],
            "events": [
                {
                    "name": "Infinity Gauntlet",
                    "content": """
The Infinity Gauntlet is a major crossover event in Marvel Comics.
Published in 1991, it was written by Jim Starlin and penciled by George Pérez and Ron Lim.

Plot:
Thanos acquires all six Infinity Gems and becomes omnipotent, wiping out half of all life in the universe.
The remaining heroes and cosmic entities must band together to stop him.

Key Characters:
- Thanos
- Adam Warlock
- Silver Surfer
- The Avengers
- The X-Men
- Various cosmic entities

Impact:
This event is considered one of the most significant in Marvel Comics history and has influenced multiple adaptations,
including the Marvel Cinematic Universe films Avengers: Infinity War and Avengers: Endgame.
                    """.strip()
                },
                {
                    "name": "Civil War",
                    "content": """
Civil War is a major crossover event in Marvel Comics.
Published in 2006-2007, it was written by Mark Millar and penciled by Steve McNiven.

Plot:
After a tragedy involving young superheroes, the U.S. government passes the Superhuman Registration Act,
requiring all superheroes to register their identities. This splits the superhero community into two factions:
those who support registration (led by Iron Man) and those who oppose it (led by Captain America).

Key Characters:
- Iron Man (pro-registration)
- Captain America (anti-registration)
- Spider-Man
- The Punisher
- Various heroes on both sides

Impact:
This event fundamentally changed the Marvel Universe and has been adapted into the Marvel Cinematic Universe
film Captain America: Civil War (2016).
                    """.strip()
                }
            ]
        }
        
        # Save all content to files
        all_files = []
        
        for category, items in marvel_content.items():
            for item in items:
                filename = re.sub(r'[^\w\s-]', '', item['name']).strip().replace(' ', '_')
                filepath = self.output_dir / f"{category}_{filename}.txt"
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"Title: {item['name']}\n")
                    f.write(f"Category: {category}\n")
                    f.write(f"\n{item['content']}\n")
                
                all_files.append({
                    'name': item['name'],
                    'category': category,
                    'file': str(filepath),
                    'content_length': len(item['content'])
                })
        
        return all_files

def main():
    """Main function to fetch Marvel documents"""
    print("🦸 Starting Marvel Document Fetching...")
    
    fetcher = MarvelDocumentFetcher()
    
    # Create content from known Marvel information
    print("\n📚 Creating Marvel content database...")
    files = fetcher.create_marvel_wiki_content()
    
    print(f"\n✅ Created {len(files)} Marvel document files")
    
    # Optionally fetch from Wikipedia (commented out to avoid rate limiting)
    # print("\n🌐 Fetching additional data from Wikipedia...")
    # characters = [
    #     "Spider-Man", "Iron Man", "Captain America", "Thor", "Hulk",
    #     "Black Widow", "Doctor Strange", "Wolverine"
    # ]
    # wiki_files = fetcher.fetch_marvel_characters(characters)
    
    # Save metadata
    metadata = {
        'total_files': len(files),
        'files': files,
        'created_at': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    metadata_path = fetcher.output_dir / 'metadata.json'
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"📄 Metadata saved to {metadata_path}")
    print("✅ Document fetching complete!")

if __name__ == "__main__":
    main()

