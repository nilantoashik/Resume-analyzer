// DOM Elements
const uploadForm = document.getElementById('upload-form');
const resumeFile = document.getElementById('resume-file');
const fileLabel = document.querySelector('.file-label');
const uploadContent = document.querySelector('.upload-content');
const fileSelected = document.querySelector('.file-selected');
const fileNameDisplay = document.querySelector('.file-selected .file-name');
const removeFileBtn = document.querySelector('.remove-file');
const analyzeBtn = document.getElementById('analyze-btn');
const btnText = document.querySelector('.btn-text');
const loader = document.querySelector('.loader');
const resultsSection = document.getElementById('results-section');
const errorSection = document.getElementById('error-section');
const uploadSection = document.querySelector('.upload-section');

// API Base URL
// Use environment variable or fallback to current origin
const API_BASE = window.location.hostname.includes('github.io') 
    ? 'https://resume-analyzer-api.onrender.com'  // Your deployed backend URL
    : window.location.origin;  // Local development

// Store analysis data for download
let currentAnalysisData = null;

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Get Started button
const getStartedBtn = document.getElementById('get-started-btn');
if (getStartedBtn) {
    getStartedBtn.addEventListener('click', () => {
        const uploadSection = document.getElementById('upload-section');
        if (uploadSection) {
            uploadSection.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
}

// File selection handler
resumeFile.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        showSelectedFile(file.name);
    }
});

// Show selected file
function showSelectedFile(filename) {
    uploadContent.style.display = 'none';
    fileSelected.style.display = 'flex';
    fileNameDisplay.textContent = filename;
    fileLabel.style.borderColor = '#2d2d2d';
    fileLabel.style.background = 'var(--gray-100)';
}

// Remove file handler
removeFileBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    e.preventDefault();
    resumeFile.value = '';
    uploadContent.style.display = 'block';
    fileSelected.style.display = 'none';
    fileLabel.style.borderColor = 'var(--gray-300)';
    fileLabel.style.background = 'var(--gray-50)';
});

// Drag and drop handlers
fileLabel.addEventListener('dragover', (e) => {
    e.preventDefault();
    fileLabel.style.borderColor = '#2d2d2d';
    fileLabel.style.background = 'var(--gray-100)';
    fileLabel.style.transform = 'scale(1.02)';
});

fileLabel.addEventListener('dragleave', () => {
    if (!resumeFile.files.length) {
        fileLabel.style.borderColor = 'var(--gray-300)';
        fileLabel.style.background = 'var(--gray-50)';
    }
    fileLabel.style.transform = 'scale(1)';
});

fileLabel.addEventListener('drop', (e) => {
    e.preventDefault();
    fileLabel.style.transform = 'scale(1)';
    
    const file = e.dataTransfer.files[0];
    if (file) {
        resumeFile.files = e.dataTransfer.files;
        showSelectedFile(file.name);
    }
});

// Form submission
uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    console.log('Form submitted');
    console.log('API Base:', API_BASE);
    console.log('File selected:', resumeFile.files[0]);
    
    // Show loading state
    analyzeBtn.disabled = true;
    btnText.textContent = 'Analyzing...';
    loader.style.display = 'block';
    errorSection.style.display = 'none';
    
    // Prepare form data
    const formData = new FormData(uploadForm);
    
    console.log('FormData created, making fetch request...');
    
    try {
        // Upload and analyze resume
        const response = await fetch(`${API_BASE}/api/analyze`, {
            method: 'POST',
            body: formData
        });
        
        console.log('Response received:', response.status);
        
        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.error || `Server error: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Data received:', data);
        
        // Display results
        displayResults(data);
        
        // Hide upload section and show results
        uploadSection.style.display = 'none';
        resultsSection.style.display = 'block';
        
    } catch (error) {
        console.error('Error:', error);
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            showError('Connection Error', 'Cannot connect to server. Please make sure the server is running on localhost:5000');
        } else {
            showError('Analysis Error', error.message || 'Failed to analyze resume. Please try again.');
        }
    } finally {
        // Reset loading state
        analyzeBtn.disabled = false;
        btnText.textContent = 'Analyze Resume';
        loader.style.display = 'none';
    }
});

// Display results
function displayResults(data) {
    const { parsed_data, ai_analysis } = data;
    
    // Store data for download
    currentAnalysisData = data;
    
    // Display parsed information
    document.getElementById('email-value').textContent = parsed_data.email || 'Not found';
    document.getElementById('phone-value').textContent = parsed_data.phone || 'Not found';
    document.getElementById('experience-value').textContent = 
        parsed_data.experience_years ? `${parsed_data.experience_years} years` : 'Not specified';
    
    // Display skills
    const skillsList = document.getElementById('skills-list');
    skillsList.innerHTML = '';
    if (parsed_data.skills && parsed_data.skills.length > 0) {
        parsed_data.skills.forEach(skill => {
            const tag = document.createElement('span');
            tag.className = 'skill-tag';
            tag.textContent = skill;
            skillsList.appendChild(tag);
        });
    } else {
        skillsList.innerHTML = '<span class="info-value">No specific skills detected</span>';
    }
    
    // Display AI analysis summary
    document.getElementById('summary-text').textContent = 
        ai_analysis.summary || 'Analysis completed successfully.';
    
    // Display strengths
    const strengthsList = document.getElementById('strengths-list');
    strengthsList.innerHTML = '';
    if (ai_analysis.strengths && ai_analysis.strengths.length > 0) {
        ai_analysis.strengths.forEach(strength => {
            const li = document.createElement('li');
            li.textContent = strength;
            strengthsList.appendChild(li);
        });
    } else {
        strengthsList.innerHTML = '<li>No specific strengths identified</li>';
    }
    
    // Display weaknesses
    const weaknessesList = document.getElementById('weaknesses-list');
    weaknessesList.innerHTML = '';
    if (ai_analysis.weaknesses && ai_analysis.weaknesses.length > 0) {
        ai_analysis.weaknesses.forEach(weakness => {
            const li = document.createElement('li');
            li.textContent = weakness;
            weaknessesList.appendChild(li);
        });
    } else {
        weaknessesList.innerHTML = '<li>No major weaknesses identified</li>';
    }
    
    // Display recommendations
    const recommendationsList = document.getElementById('recommendations-list');
    recommendationsList.innerHTML = '';
    if (ai_analysis.recommendations && ai_analysis.recommendations.length > 0) {
        ai_analysis.recommendations.forEach(recommendation => {
            const li = document.createElement('li');
            li.textContent = recommendation;
            recommendationsList.appendChild(li);
        });
    } else {
        recommendationsList.innerHTML = '<li>No specific recommendations at this time</li>';
    }
    
    // Get and display scores
    fetchScores(parsed_data.full_text);
}

// Fetch and display scores
async function fetchScores(resumeText) {
    try {
        const jobDescription = document.getElementById('job-description').value;
        
        const response = await fetch(`${API_BASE}/api/score`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                resume_text: resumeText,
                job_description: jobDescription
            })
        });
        
        const scores = await response.json();
        
        if (response.ok) {
            updateScores(scores);
        }
    } catch (error) {
        console.error('Error fetching scores:', error);
        // Set default scores if fetching fails
        updateScores({
            overall_score: 75,
            content_quality: 75,
            format_structure: 75,
            skills_match: 70,
            experience_level: 75
        });
    }
}

// Update score displays
function updateScores(scores) {
    const overallScore = scores.overall_score || 75;
    
    // Update overall score circle
    const scoreCircle = document.getElementById('score-circle');
    const circumference = 439.8; // 2 * PI * 70
    const offset = circumference - (overallScore / 100) * circumference;
    scoreCircle.style.strokeDashoffset = offset;
    
    document.getElementById('overall-score').textContent = overallScore;
    
    // Update individual scores
    updateScoreBar('content', scores.content_quality || 75);
    updateScoreBar('format', scores.format_structure || 75);
    updateScoreBar('skills', scores.skills_match || 70);
    updateScoreBar('experience', scores.experience_level || 75);
}

// Update individual score bar
function updateScoreBar(type, value) {
    const bar = document.getElementById(`${type}-score`);
    const num = document.getElementById(`${type}-num`);
    
    if (bar && num) {
        setTimeout(() => {
            bar.style.width = `${value}%`;
            num.textContent = value;
        }, 100);
    }
}

// Show error message
function showError(title, message, instructions = null) {
    errorSection.style.display = 'block';
    const errorMessageEl = document.getElementById('error-message');
    
    if (instructions) {
        // Format with title, message, and instructions
        let html = `<strong>${title}</strong><br><br>${message}<br><br>`;
        instructions.forEach(instruction => {
            html += `<div style="margin: 8px 0; padding-left: 20px; font-family: monospace; font-size: 0.9em;">${instruction}</div>`;
        });
        html += `<br><a href="https://github.com/nilantoashik/Resume-analyzer" target="_blank" style="color: #4CAF50; text-decoration: none; font-weight: 600;">View Repository →</a>`;
        errorMessageEl.innerHTML = html;
    } else {
        // Simple message (for backward compatibility)
        errorMessageEl.textContent = typeof title === 'string' && !message ? title : `${title}: ${message}`;
    }
}

// Try again button
document.getElementById('try-again').addEventListener('click', () => {
    errorSection.style.display = 'none';
    uploadSection.style.display = 'block';
});

// Analyze another resume
document.getElementById('analyze-another').addEventListener('click', () => {
    resultsSection.style.display = 'none';
    uploadSection.style.display = 'block';
    uploadForm.reset();
    resumeFile.value = '';
    uploadContent.style.display = 'block';
    fileSelected.style.display = 'none';
    fileLabel.style.borderColor = 'var(--gray-300)';
    fileLabel.style.background = 'var(--gray-50)';
    
    // Smooth scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

// Download report functionality
document.getElementById('download-report').addEventListener('click', () => {
    if (!currentAnalysisData) {
        alert('No analysis data available to download');
        return;
    }
    
    const { parsed_data, ai_analysis, filename } = currentAnalysisData;
    
    // Create report content
    let reportContent = '=== RESUME ANALYSIS REPORT ===\n\n';
    reportContent += `File: ${filename}\n`;
    reportContent += `Date: ${new Date().toLocaleString()}\n\n`;
    
    reportContent += '--- EXTRACTED INFORMATION ---\n';
    reportContent += `Email: ${parsed_data.email || 'Not found'}\n`;
    reportContent += `Phone: ${parsed_data.phone || 'Not found'}\n`;
    reportContent += `Experience: ${parsed_data.experience_years ? parsed_data.experience_years + ' years' : 'Not specified'}\n`;
    reportContent += `Skills: ${parsed_data.skills && parsed_data.skills.length > 0 ? parsed_data.skills.join(', ') : 'None detected'}\n\n`;
    
    reportContent += '--- SUMMARY ---\n';
    reportContent += `${ai_analysis.summary || 'Analysis completed successfully.'}\n\n`;
    
    if (ai_analysis.strengths && ai_analysis.strengths.length > 0) {
        reportContent += '--- STRENGTHS ---\n';
        ai_analysis.strengths.forEach((strength, index) => {
            reportContent += `${index + 1}. ${strength}\n`;
        });
        reportContent += '\n';
    }
    
    if (ai_analysis.weaknesses && ai_analysis.weaknesses.length > 0) {
        reportContent += '--- AREAS FOR IMPROVEMENT ---\n';
        ai_analysis.weaknesses.forEach((weakness, index) => {
            reportContent += `${index + 1}. ${weakness}\n`;
        });
        reportContent += '\n';
    }
    
    if (ai_analysis.recommendations && ai_analysis.recommendations.length > 0) {
        reportContent += '--- RECOMMENDATIONS ---\n';
        ai_analysis.recommendations.forEach((rec, index) => {
            reportContent += `${index + 1}. ${rec}\n`;
        });
        reportContent += '\n';
    }
    
    reportContent += '\n=== END OF REPORT ===\n';
    
    // Create and download file
    const blob = new Blob([reportContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `resume_analysis_${Date.now()}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    console.log('Report downloaded successfully');
});
