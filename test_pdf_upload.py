import requests

url = 'http://localhost:5000/api/analyze'

# Open the PDF file
with open('test_resume.pdf', 'rb') as f:
    files = {'resume': ('test_resume.pdf', f, 'application/pdf')}
    data = {'job_description': ''}
    
    response = requests.post(url, files=files, data=data)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
