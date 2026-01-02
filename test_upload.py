import requests

# Test file upload
url = "http://localhost:5000/api/analyze"

# Create a dummy text file to test
with open('test_resume.txt', 'w') as f:
    f.write("""
    John Doe
    Email: john.doe@example.com
    Phone: (555) 123-4567
    
    EXPERIENCE
    Software Engineer at Tech Corp
    2020-Present
    - Developed Python applications
    - Worked with Flask and Django
    
    SKILLS
    Python, JavaScript, React, Node.js, SQL
    
    EDUCATION
    Bachelor of Science in Computer Science
    University of Technology, 2020
    """)

# Try to upload
try:
    with open('test_resume.txt', 'rb') as f:
        files = {'resume': ('test_resume.txt', f, 'text/plain')}
        data = {'job_description': 'Looking for a Python developer'}
        
        response = requests.post(url, files=files, data=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
