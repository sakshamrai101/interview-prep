"""
Escape the Maze

- interviewer gives: starting_url endpoint 
- script that hits this page 
- handles different payloads and recursively navigates until it hits an 'exit' payload condition 

- we have inherent chaos in the system: 
    - a node might return clean JSON, plain unformatted text containing embedded links, 
    or a raw dictionary mapping keys arbitrarirly 
    - dynamic url schemas (some are absolute paths http://....) others will be relative fragments (/path/node) 
    and some swap protocols entierly 
    - network fault handling: System throws 404 not found, 302/301 Redirect blocks or empty payloads that require 
    immediate dead-end detection and backtracking. 
"""

import urllib.request
import urllib.parse
import json
import re

class AutonomousMazeClient:
    def __init__(self, start_url: str):

        self.start_url = start_url 

        # Track already visited nodes to prevent cyclic loops in memory graph 
        self.visited_nodes = set()
        self.exit_payload = None 

    
    def normalize_url(self, current_url: str, extracted_path: str) -> str:
        """ Resolves relative path anchors into absolute fully formed URLS."""

        new_path = extracted_path.strip()

        # Handles raw fragments like /node/34 seamlessly relative to its caller parent 
        return urllib.parse.urljoin(current_url, new_path)
    
    def fetch_node_safely(self, url: str) -> tuple:
        """
        Executes raw HTTP requests. 
        Handles 3xx redirects, 4xx/5xx errors, and safely decodes heterogenous payloads. 

        """
        try:
            req = urllib.request.Request(
                url,
                headers={'User-Agent': 'Maze-Runner-Agent/1.0'}
            )

            with urllib.request.urlopen(req, timeout=5) as response:
                final_url = response.geturl()
                raw_data = response.read()
                content_type = response.headers.get('Content-Type', '')
            
            return raw_data, final_url, content_type
        
        except urllib.error.HTTPError as e:
            # Interviewer Edge-Case: Catch dead ends buried inside 404/500 code wrapppers 
            print(f"[HTTP ERROR] Encountered status {e.code} at target node: {url}")
            return None, url, ""
        
        except Excpetion as e:
            print(f"[NETWORK FAULT] Unbale to open link connection: {url}. Error: {str(e)}")
            return None, url, ""
    
    def extract_links_polymorphically(self, raw_bytes: bytes, content_type: str) -> list:
        """ Parses response data fields across variable content encodings on the fly """
        if not raw_byte:
            return []
        
        links = []

        try:
            # Decoding raw payload to a working string representation
            decoded_string = raw_bytes.decode('utf-8')

            # Variant 1: JSON structure 
            if 'application/json' in content_type or decoded_string.strip().startswith(('{', '[')):
                data = json.loads(decoded_string)


                # Check for absolute win condition flag 
                if isinstance(data, dict):
                    if data.get("status") == "EXIT" or "exit_key" in data:
                        self.exit_payload = data 
                        return ["WIN"]
                    

                    # Extract keys holding link patterns dynamically 
                    for val in data.values():
                        if isinstance(val, str) and ('/' in val or 'http' in val):
                            links.append(val)
                        
                    if "links" in data and isinstance(data["links"], list):
                        links.extend(data["links"])
            
            # Variant 2: Plain Text / Markup fallbacks 
            else:
                # Fallback to a regex matching pattern to harvest url links embedded 
                if "exit" in decoded_string:
                    self.exit_payload = {"raw_text": decoded_string}
                    return ["WIN"]
                
                # Scrapes tokens containing slash fragments or network patterns 
                found_tokens = re.findall(r'(?:https?://\S+|/[\w\-\./]+)', decoded_string)
                links.extend(found_tokens)
        
        except Exception as parse_error:
        print(f" [PARSING EXCEPTION] Skipping corrupted node layer. Error: {str(parse_error)}")

        return list(set(links)) # returns deduplicated link array
    
    def traverse(self, current_url: str) -> bool:

        """ DFS recursive traversal layout """


        if current_url in self.visited_nodes:
            return False 
        
        print(f"Crawling Target Node: {current_url}")

        self.visited_nodes.add(current_url)

        # 1. Fire http request and fetch node components 
        raw_bytes, finalized_url, content_type = self.fetch_node_safely(current_url)
        if not raw_bytes:
            return False # dead end node, backtrack 
        
        # 2. Extract potential paths 
        discovered_paths = self.extract_links_polymorphically(raw_bytes, content_type)

        # Win checkpoint evaluation:
        if "WIN" in discovered_paths:
            print("\n🎯 [TARGET ACQUIRED] Found the exit node entry point!")
            return True 
        
        # 3. Recursively step into child nodes
        for path in discovered_paths:
            resolved_next_step = self.normalize_url(finalized_url, path)
        
            # Safeguard: Avoid bouncing infinitely out of the sandboz zone.
            if "localhost" in resolved_next_step or "mock-maze" in resolved_next_step:
                if resolved_next_step not in self.visited_nodes:
                    if self.traverse(resolved_next_step):
                        return True 
        return False 

def run(self):
    print(f"Starting escape algorithm initialisation at root endpoint: {self.stack_url}")
    success = self.traversal(self, self.start_url)

    if success:
        print(f"🏆 System successfully escaped the grid network cluster!")
        print(f"Exit Node Details: {self.exit_payload}")
    else:
        print("❌ Traceback path exhaustively evaluated. All paths hit dead-ends.")