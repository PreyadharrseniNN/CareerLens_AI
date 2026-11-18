import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

def load_json(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Could not load {filepath}: {e}")
        return {}

JOB_ROLES_MAP = load_json(os.path.join(DATA_DIR, 'job_roles.json'))

def recommend_jobs(extracted_skills):
    """
    Recommends jobs based on the intersection of extracted skills
    and the skills required for specific roles.
    Returns a list of roles sorted by match percentage.
    """
    extracted_lower = set([s.lower() for s in extracted_skills])
    
    recommendations = []
    for role, required_skills in JOB_ROLES_MAP.items():
        matched = [s for s in required_skills if s.lower() in extracted_lower]
        match_count = len(matched)
        
        if match_count > 0 and len(required_skills) > 0:
            match_percentage = int((match_count / len(required_skills)) * 100)
            recommendations.append({
                "role": role,
                "match": match_percentage,
                "matched_skills": matched,
                "required_skills": required_skills
            })
            
    # Sort by match percentage descending
    recommendations = sorted(recommendations, key=lambda x: x['match'], reverse=True)
    return recommendations[:3]  # Return top 3
    
def generate_roadmap(job_recommendations, extracted_skills):
    """
    Generates a structured career roadmap based on the top job recommendation.
    Suggests missing skills to learn over 3, 6, and 12 months.
    """
    if not job_recommendations:
        return "Not enough data to generate a roadmap. Try adding more skills to your resume."
        
    top_job = job_recommendations[0]
    role = top_job['role']
    required = JOB_ROLES_MAP.get(role, [])
    have = set([s.lower() for s in extracted_skills])
    
    # Preserve proper capitalization from JOB_ROLES_MAP
    missing = [s for s in required if s.lower() not in have]
    
    if not missing:
        return f"You have an excellent profile for {role}! Continue building advanced projects to solidify your skills."
        
    # Split missing skills into timeframes
    roadmap = f"Roadmap to becoming a stronger {role}:\n"
    if len(missing) > 0:
        roadmap += f"- Next 3 Months: Focus on learning {', '.join(missing[:2])}.\n"
    if len(missing) > 2:
        roadmap += f"- 6 Months: Build projects using {', '.join(missing[2:4])}.\n"
    if len(missing) > 4:
        roadmap += f"- 1 Year: Master {', '.join(missing[4:])}."
        
    return roadmap.strip()
