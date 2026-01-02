import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from resume_parser import ResumeParser
from ai_analyzer import AIAnalyzer

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}

# Initialize services
resume_parser = ResumeParser()
ai_analyzer = AIAnalyzer(api_key=os.getenv('OPENAI_API_KEY'))

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_fallback_analysis(resume_data, resume_text):
    """Generate comprehensive deep analysis when AI is unavailable"""
    strengths = []
    weaknesses = []
    recommendations = []
    
    text_lower = resume_text.lower()
    words = resume_text.split()
    word_count = len(words)
    
    # ============ CONTACT INFORMATION ANALYSIS ============
    if resume_data.get('email'):
        email = resume_data['email']
        if any(unprofessional in email.lower() for unprofessional in ['sexy', 'cute', 'cool', 'baby', '123', '69', '420']):
            weaknesses.append("Email address may appear unprofessional")
            recommendations.append("Consider using a professional email format: firstname.lastname@domain.com")
        else:
            strengths.append("Professional email address is clearly visible for recruiter contact")
    else:
        weaknesses.append("Email address is missing or not detectable - critical contact information")
        recommendations.append("Add a professional email address at the top: firstname.lastname@gmail.com")
    
    if resume_data.get('phone'):
        strengths.append("Phone number provided for direct communication")
    else:
        weaknesses.append("Phone number not found - missing important contact method")
        recommendations.append("Include a phone number with area code for easy callback")
    
    # ============ SKILLS ANALYSIS (DEEP) ============
    skills = resume_data.get('skills', [])
    skills_count = len(skills)
    
    # Categorize skills
    tech_skills = [s for s in skills if any(tech in s.lower() for tech in ['python', 'java', 'javascript', 'sql', 'react', 'node', 'c++', 'c#', 'aws', 'docker', 'kubernetes', 'git', 'html', 'css', 'api', 'django', 'flask', 'angular', 'vue', 'typescript', 'mongodb', 'postgresql', 'mysql', 'redis', 'kafka', 'spark', 'hadoop', 'tensorflow', 'pytorch', 'scikit', 'pandas', 'numpy'])]
    
    if skills_count >= 8:
        strengths.append(f"Comprehensive skills section with {skills_count} identified skills demonstrating versatility")
        if len(tech_skills) >= 5:
            strengths.append(f"Strong technical skill set with {len(tech_skills)} modern technologies")
    elif skills_count >= 5:
        strengths.append(f"Adequate skills listed ({skills_count} skills)")
        if len(tech_skills) < 3:
            recommendations.append("Add more in-demand technical skills relevant to your target role (e.g., cloud platforms, modern frameworks)")
    elif skills_count > 0:
        weaknesses.append(f"Limited skills section with only {skills_count} skills - appears thin")
        recommendations.append("Expand skills section to 8-12 items including technical skills, soft skills, and certifications")
    else:
        weaknesses.append("No skills section detected - major gap in resume")
        recommendations.append("Create a prominent skills section listing technical proficiencies, tools, and competencies")
    
    # Check for soft skills
    soft_skills_keywords = ['leadership', 'communication', 'teamwork', 'problem-solving', 'analytical', 'management', 'collaboration', 'presentation']
    has_soft_skills = any(skill in text_lower for skill in soft_skills_keywords)
    if not has_soft_skills:
        recommendations.append("Include soft skills like Leadership, Communication, and Problem-Solving to show well-rounded capabilities")
    
    # ============ CONTENT QUALITY & LENGTH ANALYSIS ============
    if 400 <= word_count <= 600:
        strengths.append(f"Optimal resume length ({word_count} words) - concise yet comprehensive")
    elif 300 <= word_count < 400:
        weaknesses.append(f"Resume is somewhat brief ({word_count} words) - may lack sufficient detail")
        recommendations.append("Expand bullet points with more context about responsibilities, technologies used, and impact created")
    elif word_count < 300:
        weaknesses.append(f"Resume is too short ({word_count} words) - appears incomplete or lacking detail")
        recommendations.append("Add 2-3 bullet points per role describing key achievements, technologies, and quantifiable results")
    elif 600 < word_count <= 900:
        strengths.append("Resume has substantial content describing experience")
        recommendations.append("Consider condensing to most impactful points to keep recruiter attention")
    else:
        weaknesses.append(f"Resume may be too lengthy ({word_count} words) - risk of losing reader attention")
        recommendations.append("Streamline content to 1-2 pages, focusing on most recent and relevant experiences")
    
    # ============ WORK EXPERIENCE ANALYSIS (DEEP) ============
    work_experience = resume_data.get('work_experience', [])
    has_experience = any(keyword in text_lower for keyword in ['experience', 'employment', 'work history', 'professional experience', 'career'])
    
    if work_experience and len(work_experience) > 0:
        # Analyze number of roles
        num_roles = len(work_experience)
        if num_roles >= 3:
            strengths.append(f"Strong work history with {num_roles} distinct roles showing career progression")
        elif num_roles >= 2:
            strengths.append(f"Work experience section includes {num_roles} professional roles")
        else:
            strengths.append("Work experience is present and structured")
            recommendations.append("If you have more roles, include them to show broader experience (aim for 2-4 recent positions)")
        
        # Analyze duration and dates
        roles_with_dates = [exp for exp in work_experience if exp.get('date_range')]
        if len(roles_with_dates) >= num_roles * 0.8:  # 80% have dates
            strengths.append("Employment dates clearly specified for all roles - shows timeline and tenure")
        elif roles_with_dates:
            weaknesses.append("Some work experiences missing date ranges")
            recommendations.append("Add dates (MM/YYYY - MM/YYYY or Present) to all work experiences for clarity")
        else:
            weaknesses.append("Work experience lacks date information - dates are critical for recruiters")
            recommendations.append("Add employment dates in format: 'June 2022 - Present' or '01/2022 - 12/2023'")
        
        # Check for recent/current experience
        total_duration = sum([exp.get('duration_years', 0) for exp in work_experience if exp.get('duration_years')])
        if total_duration >= 5:
            strengths.append(f"Substantial work experience totaling approximately {total_duration}+ years in the field")
        elif total_duration >= 2:
            strengths.append(f"Relevant work experience spanning {total_duration}+ years")
        
        # Analyze bullet points per role
        avg_bullets = sum([exp.get('bullet_points', 0) for exp in work_experience]) / len(work_experience) if work_experience else 0
        if avg_bullets >= 4:
            strengths.append("Each role has detailed bullet points (4+) describing responsibilities and achievements")
        elif avg_bullets >= 2:
            recommendations.append("Expand bullet points to 4-6 per role with specific accomplishments and technologies used")
        else:
            weaknesses.append("Work experience entries lack sufficient detail and bullet points")
            recommendations.append("Add 4-6 bullet points per role: responsibilities, achievements, metrics, technologies, impact")
        
        # Check for job title clarity
        roles_with_clear_titles = sum([1 for exp in work_experience if any(keyword in exp.get('title_line', '').lower() for keyword in ['engineer', 'developer', 'manager', 'analyst', 'designer', 'architect', 'director', 'lead', 'senior'])])
        if roles_with_clear_titles >= len(work_experience):
            strengths.append("Job titles clearly stated for all positions - easy to understand your roles")
        elif roles_with_clear_titles < len(work_experience) * 0.5:
            weaknesses.append("Some job titles unclear or missing - makes it hard to understand your roles")
            recommendations.append("Ensure each role has a clear job title: 'Senior Software Engineer', 'Product Manager', etc.")
    
    elif has_experience:
        strengths.append("Work experience section is present in resume")
        weaknesses.append("Work experience details are not clearly structured - difficult to parse roles and timeline")
        recommendations.append("Format experience as: Job Title | Company Name | Dates\n• Bullet point 1\n• Bullet point 2")
    else:
        weaknesses.append("Experience/Work history section missing or not detectable - this is CRITICAL content")
        recommendations.append("Add a prominent 'PROFESSIONAL EXPERIENCE' section with company names, job titles, dates, and 4-6 bullet points per role")
        recommendations.append("Use this format: [Job Title] at [Company] | [Start Date] - [End Date]")
    
    # ============ OTHER SECTIONS ANALYSIS ============
    has_education = any(keyword in text_lower for keyword in ['education', 'degree', 'university', 'college', 'bachelor', 'master', 'phd', 'diploma'])
    has_projects = any(keyword in text_lower for keyword in ['project', 'portfolio', 'built', 'developed', 'created'])
    has_certifications = any(keyword in text_lower for keyword in ['certification', 'certified', 'certificate', 'credential'])
    
    if has_education:
        education_entries = resume_data.get('education', [])
        if len(education_entries) >= 1:
            strengths.append(f"Educational background clearly presented with degree information")
        else:
            strengths.append("Education section is present in resume")
    else:
        weaknesses.append("Education section not found - missing important qualification information")
        recommendations.append("Include EDUCATION section: Degree | Institution | Graduation Year | GPA (if 3.5+)")
    
    if has_projects:
        project_count = text_lower.count('project')
        if project_count >= 3:
            strengths.append("Multiple projects showcased - demonstrates hands-on experience and initiative")
        else:
            strengths.append("Projects or portfolio work mentioned - demonstrates practical application")
    else:
        if 'engineer' in text_lower or 'developer' in text_lower or 'designer' in text_lower:
            recommendations.append("Add PROJECTS section with 2-4 projects: brief description, technologies used, outcomes/impact")
    
    if has_certifications:
        strengths.append("Professional certifications included - adds credibility and shows continuous learning")
    else:
        recommendations.append("Consider adding CERTIFICATIONS section (AWS, Azure, PMP, Scrum, Google Analytics, etc.)")
    
    # ============ ACHIEVEMENT & IMPACT ANALYSIS ============
    action_verbs = ['achieved', 'improved', 'increased', 'reduced', 'developed', 'implemented', 'designed', 'led', 'managed', 'delivered', 'created', 'optimized', 'streamlined', 'launched', 'spearheaded', 'drove', 'executed', 'established', 'built', 'engineered']
    action_verb_count = sum(1 for verb in action_verbs if verb in text_lower)
    
    if action_verb_count >= 5:
        strengths.append(f"Strong use of action verbs ({action_verb_count} found) - demonstrates proactive contributions")
    elif action_verb_count >= 3:
        strengths.append("Good use of action-oriented language")
    else:
        weaknesses.append("Limited use of strong action verbs - resume may appear passive")
        recommendations.append("Start bullet points with power verbs: Developed, Implemented, Achieved, Led, Optimized, Delivered")
    
    # Check for quantifiable metrics
    percentage_mentions = resume_text.count('%')
    number_mentions = sum(1 for char in resume_text if char.isdigit())
    
    if percentage_mentions >= 2 or number_mentions >= 10:
        strengths.append("Quantifiable metrics and data points included - demonstrates measurable impact")
    else:
        weaknesses.append("Lacks quantifiable achievements and metrics")
        recommendations.append("Add numbers and metrics: 'Increased efficiency by 40%', 'Managed team of 8', 'Reduced costs by $50K'")
    
    # ============ KEYWORD OPTIMIZATION ANALYSIS ============
    industry_keywords = {
        'tech': ['agile', 'scrum', 'ci/cd', 'api', 'microservices', 'cloud', 'devops', 'full-stack', 'backend', 'frontend'],
        'business': ['roi', 'kpi', 'strategy', 'stakeholder', 'revenue', 'growth', 'market', 'analysis'],
        'management': ['leadership', 'team', 'budget', 'project', 'cross-functional', 'strategic', 'planning']
    }
    
    keyword_matches = 0
    for category, keywords in industry_keywords.items():
        keyword_matches += sum(1 for keyword in keywords if keyword in text_lower)
    
    if keyword_matches >= 5:
        strengths.append("Good use of industry-relevant keywords - ATS-friendly and recruiter-optimized")
    elif keyword_matches >= 3:
        recommendations.append("Include more industry keywords to improve ATS (Applicant Tracking System) compatibility")
    else:
        weaknesses.append("Few industry-specific keywords detected - may not pass ATS screening")
        recommendations.append("Research job descriptions and incorporate relevant keywords: cloud, agile, stakeholder, API, leadership")
    
    # ============ FORMAT & STRUCTURE ANALYSIS ============
    has_bullets = any(char in resume_text for char in ['•', '●', '◦', '-', '*'])
    if has_bullets:
        strengths.append("Bullet points used effectively for readability and scanning")
    else:
        weaknesses.append("No bullet points detected - content may be hard to scan")
        recommendations.append("Use bullet points to break down responsibilities and achievements for better readability")
    
    # Check for dates
    date_patterns = ['2020', '2021', '2022', '2023', '2024', '2025', '2026', 'present', 'current']
    has_dates = any(pattern in text_lower for pattern in date_patterns)
    if has_dates:
        strengths.append("Timeline and dates included - shows career progression")
    else:
        recommendations.append("Add dates (MM/YYYY format) to all experiences and education entries")
    
    # ============ PROFESSIONAL POLISH ANALYSIS ============
    unprofessional_words = ['i', 'my', 'me', 'we', 'our', 'stuff', 'things', 'basically', 'kinda', 'sorta']
    first_person_count = sum(1 for word in unprofessional_words if f' {word} ' in text_lower)
    
    if first_person_count > 3:
        weaknesses.append("Excessive use of first-person pronouns or casual language")
        recommendations.append("Remove 'I', 'my', 'we' - use direct statements: 'Developed solutions' not 'I developed solutions'")
    elif first_person_count == 0:
        strengths.append("Professional third-person writing style maintained throughout")
    
    # Check resume length in pages (approximate)
    estimated_pages = word_count / 400
    if estimated_pages > 2.5:
        weaknesses.append(f"Resume likely exceeds 2 pages (approximately {estimated_pages:.1f} pages)")
        recommendations.append("Trim to 1-2 pages by removing older or less relevant experiences")
    
    # ============ MISSING ELEMENTS CHECK ============
    if 'linkedin' not in text_lower and 'github' not in text_lower:
        recommendations.append("Add LinkedIn profile URL and GitHub/portfolio links to increase credibility and showcase work")
    
    if 'summary' not in text_lower and 'objective' not in text_lower:
        recommendations.append("Consider adding a 3-4 line professional summary at the top highlighting key strengths and career goals")
    
    # ============ GENERATE COMPREHENSIVE SUMMARY ============
    summary = f"Comprehensive resume analysis completed. Identified {len(strengths)} key strengths and {len(weaknesses)} areas requiring attention. "
    
    if skills_count > 0:
        summary += f"Detected {skills_count} skills across various domains. "
    
    if action_verb_count >= 5:
        summary += "Strong achievement-oriented language observed. "
    
    if keyword_matches >= 5:
        summary += "Good keyword optimization for ATS systems. "
    
    if word_count < 300:
        summary += "Resume requires substantial expansion with detailed experiences. "
    elif word_count > 900:
        summary += "Consider condensing content for improved impact. "
    else:
        summary += "Resume length is within acceptable range. "
    
    summary += f"Review {len(recommendations)} specific recommendations below to enhance your resume's competitiveness and increase interview callbacks."
    
    # Ensure minimum content in each section
    if not strengths:
        strengths.append("Resume structure has been successfully parsed and core information extracted")
    if not weaknesses:
        weaknesses.append("Continue refining content to stay current with industry trends")
    if not recommendations:
        recommendations.append("Maintain resume updates quarterly with new skills, achievements, and experiences")
    
    return {
        'summary': summary,
        'strengths': strengths,
        'weaknesses': weaknesses,
        'recommendations': recommendations
    }

@app.route('/')
def index():
    """Serve the main page"""
    with open('static/index.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    from flask import send_from_directory
    return send_from_directory('.', path)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Resume Analyzer API is running'}), 200

@app.route('/api/analyze', methods=['POST'])
def analyze_resume():
    """Analyze a resume file"""
    try:
        # Check if file is present
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file provided'}), 400
        
        file = request.files['resume']
        job_description = request.form.get('job_description', '')
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check file type
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only PDF and DOCX files are allowed'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Parse resume
            resume_text = resume_parser.extract_text(filepath)
            resume_data = resume_parser.parse_resume(resume_text)
            
            # Analyze with AI
            analysis = ai_analyzer.analyze_resume(resume_text, job_description)
            
            # If AI analysis failed or returned empty data, provide fallback analysis
            if (not analysis.get('strengths') and not analysis.get('weaknesses') 
                and not analysis.get('recommendations')):
                analysis = generate_fallback_analysis(resume_data, resume_text)
            
            # Combine results
            result = {
                'parsed_data': resume_data,
                'ai_analysis': analysis,
                'filename': filename
            }
            
            return jsonify(result), 200
        
        finally:
            # Clean up uploaded file
            if os.path.exists(filepath):
                os.remove(filepath)
    
    except Exception as e:
        return jsonify({'error': f'Error analyzing resume: {str(e)}'}), 500

@app.route('/api/score', methods=['POST'])
def score_resume():
    """Score a resume against a job description"""
    try:
        data = request.get_json()
        resume_text = data.get('resume_text', '')
        job_description = data.get('job_description', '')
        
        if not resume_text:
            return jsonify({'error': 'Resume text is required'}), 400
        
        # Get scoring from AI
        score_analysis = ai_analyzer.score_resume(resume_text, job_description)
        
        return jsonify(score_analysis), 200
    
    except Exception as e:
        return jsonify({'error': f'Error scoring resume: {str(e)}'}), 500

@app.route('/api/suggestions', methods=['POST'])
def get_suggestions():
    """Get improvement suggestions for a resume"""
    try:
        data = request.get_json()
        resume_text = data.get('resume_text', '')
        job_description = data.get('job_description', '')
        
        if not resume_text:
            return jsonify({'error': 'Resume text is required'}), 400
        
        # Get suggestions from AI
        suggestions = ai_analyzer.get_suggestions(resume_text, job_description)
        
        return jsonify(suggestions), 200
    
    except Exception as e:
        return jsonify({'error': f'Error getting suggestions: {str(e)}'}), 500

if __name__ == '__main__':
    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Run app
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
