import requests
import json

def test_detailed_resume():
    url = 'http://localhost:5000/api/analyze'
    
    # Open and send the detailed test resume
    with open('test_detailed_resume.pdf', 'rb') as f:
        files = {'resume': ('test_detailed_resume.pdf', f, 'application/pdf')}
        data = {'job_description': 'Looking for a Senior Software Engineer with Python and AWS experience'}
        
        response = requests.post(url, files=files, data=data)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("\n========== ANALYSIS RESULTS ==========\n")
            
            # Print parsed data
            print("--- PARSED DATA ---")
            parsed = result.get('parsed_data', {})
            print(f"Email: {parsed.get('email')}")
            print(f"Phone: {parsed.get('phone')}")
            print(f"Experience Years: {parsed.get('experience_years')}")
            print(f"Skills Found: {len(parsed.get('skills', []))}")
            print(f"Work Experience Entries: {len(parsed.get('work_experience', []))}")
            
            if parsed.get('work_experience'):
                print("\nWORK EXPERIENCE DETAILS:")
                for i, exp in enumerate(parsed.get('work_experience', []), 1):
                    print(f"\n  Job #{i}:")
                    print(f"    Title/Company: {exp.get('title_line', 'N/A')[:80]}")
                    print(f"    Date Range: {exp.get('date_range', 'Not found')}")
                    print(f"    Duration: {exp.get('duration_years', 'N/A')} years")
                    print(f"    Bullet Points: {exp.get('bullet_points', 0)}")
            
            # Print AI analysis
            print("\n--- AI ANALYSIS ---")
            analysis = result.get('ai_analysis', {})
            print(f"\nSummary: {analysis.get('summary', 'N/A')}")
            
            print(f"\nStrengths ({len(analysis.get('strengths', []))}):")
            for strength in analysis.get('strengths', [])[:10]:
                print(f"  • {strength}")
            
            print(f"\nWeaknesses ({len(analysis.get('weaknesses', []))}):")
            for weakness in analysis.get('weaknesses', [])[:5]:
                print(f"  • {weakness}")
            
            print(f"\nRecommendations ({len(analysis.get('recommendations', []))}):")
            for rec in analysis.get('recommendations', [])[:8]:
                print(f"  • {rec}")
        else:
            print(f"Error Response: {response.text}")

if __name__ == "__main__":
    test_detailed_resume()
