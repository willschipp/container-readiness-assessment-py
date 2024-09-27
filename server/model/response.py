import json

from dataclasses import dataclass

from typing import List

@dataclass
class Part:
    text: str

@dataclass
class Content:
    parts: List[Part]

@dataclass
class Candidate:
    content: Content

@dataclass
class GeminiResponse:
    candidates: List[Candidate]

def parse_json_to_gemini_response(json_string: str) -> GeminiResponse:
    # Parse the JSON string into a dictionary
    data = json.loads(json_string)
    
    # Create a list of Candidate objects from the parsed data
    candidates = []
    for candidate_data in data.get('candidates', []):
        parts = [Part(text=part['text']) for part in candidate_data['content'].get('parts', [])]
        content = Content(parts=parts)
        candidate = Candidate(content=content)
        candidates.append(candidate)
        
    return GeminiResponse(candidates=candidates)