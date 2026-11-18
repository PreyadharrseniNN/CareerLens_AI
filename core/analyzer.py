import json
import os
import re

# NLP placeholder message
print("Using intelligent regex-enhanced matching for NLP tasks.")
nlp = None

def load_json(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Could not load {filepath}: {e}")
        return {}

# Load datasets
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

try:
    KNOWN_SKILLS = load_json(os.path.join(DATA_DIR, 'skills.json'))
    if isinstance(KNOWN_SKILLS, dict):
        KNOWN_SKILLS = list(KNOWN_SKILLS.keys())
    OBSOLETE_SKILLS_MAP = load_json(os.path.join(DATA_DIR, 'obsolete_skills.json'))
    PERSONALITY_MAP = load_json(os.path.join(DATA_DIR, 'personality_traits.json'))
except Exception:
    KNOWN_SKILLS = []
    OBSOLETE_SKILLS_MAP = {}
    PERSONALITY_MAP = {}

def clean_text(text):
    """Basic text cleanup, converting to lowercase."""
    return text.lower()

def extract_skills(text):
    """
    Extracts skills by matching known and obsolete skills against the text.
    Uses boundary-aware regex to prevent false substring matches (e.g., 'Java' in 'JavaScript').
    """
    cleaned_text = clean_text(text)
    extracted = []
    
    # Merge known skills and obsolete skills map keys to ensure all are detected
    candidate_skills = {}
    for s in KNOWN_SKILLS:
        candidate_skills[s.lower()] = s
    for obs in OBSOLETE_SKILLS_MAP.keys():
        if obs.lower() not in candidate_skills:
            candidate_skills[obs.lower()] = obs

    for skill_lower, original_skill in candidate_skills.items():
        # Match with boundaries (punctuation, whitespace, or start/end of string)
        pattern = r'(?:(?<=[\s,.;:()\[\]{}<>/\\|!?"\'-])|^)' + re.escape(skill_lower) + r'(?:(?=[\s,.;:()\[\]{}<>/\\|!?"\'-])|$)'
        if re.search(pattern, cleaned_text):
            extracted.append(original_skill)
            
    return sorted(list(set(extracted)))

def detect_obsolete_skills(extracted_skills):
    """
    Checks the extracted skills against the obsolete skills mapping.
    Returns a dictionary of found obsolete skills and their modern alternatives.
    """
    obsolete_found = {}
    for skill in extracted_skills:
        for obs, modern in OBSOLETE_SKILLS_MAP.items():
            if skill.lower() == obs.lower():
                obsolete_found[obs] = modern
    return obsolete_found

def analyze_personality(text):
    """
    Matches keywords in the text to personality traits using word boundaries.
    """
    cleaned_text = clean_text(text)
    traits = []
    for trait, keywords in PERSONALITY_MAP.items():
        for keyword in keywords:
            pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
            if re.search(pattern, cleaned_text):
                traits.append(trait)
                break
    return traits

def calculate_career_score(skills, traits):
    """
    Calculates a simple multi-factor career score.
    Based on number of skills and traits.
    Max score is 100.
    """
    skill_score = min(len(skills) * 5, 70)  # max 70 points from skills (14 skills needed)
    trait_score = min(len(traits) * 6, 30)  # max 30 points from traits (5 traits needed)
    
    total_score = skill_score + trait_score
    
    explanation = f"Score of {total_score}/100. Technical skills contributed {skill_score} points. Soft skills/Traits contributed {trait_score} points."
    
    return total_score, explanation
