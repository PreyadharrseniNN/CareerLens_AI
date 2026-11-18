import os
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from core.parser import extract_text
from core.analyzer import extract_skills, detect_obsolete_skills, analyze_personality, calculate_career_score
from core.recommender import recommend_jobs, generate_roadmap

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'careerlens_super_secret_key_2026')

# Configure upload settings
UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max 16MB file limit

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if request.method == 'GET':
        return redirect(url_for('index'))
        
    if 'resume' not in request.files:
        flash('No file part provided.')
        return redirect(url_for('index'))
        
    file = request.files['resume']
    
    if file.filename == '':
        flash('Please select a resume file to upload.')
        return redirect(url_for('index'))
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        # Read text from stream
        text = extract_text(file.stream, filename)
        
        if not text or not text.strip():
            flash('Could not extract readable text from the uploaded document. Please check the file formatting.')
            return redirect(url_for('index'))
            
        # 1. Extract Skills
        skills = extract_skills(text)
        
        # 2. Detect Obsolete Skills
        obsolete = detect_obsolete_skills(skills)
        
        # 3. Analyze Personality / Soft Traits
        traits = analyze_personality(text)
        
        # 4. Calculate Career Score
        score, explanation = calculate_career_score(skills, traits)
        
        # 5. Job Recommendations
        jobs = recommend_jobs(skills)
        
        # 6. Generate Roadmap
        roadmap = generate_roadmap(jobs, skills)
        
        # Prepare results
        results = {
            "skills": skills,
            "obsolete": obsolete,
            "traits": traits,
            "score": score,
            "explanation": explanation,
            "jobs": jobs,
            "roadmap": roadmap
        }
        
        return render_template('result.html', results=results)
        
    else:
        flash('Invalid file type. Please upload a PDF or DOCX file.')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
