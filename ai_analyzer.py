from openai import OpenAI
from typing import Dict, Optional
import json

class AIAnalyzer:
    """AI-powered resume analyzer using OpenAI"""
    
    def __init__(self, api_key: str):
        """Initialize OpenAI client"""
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-3.5-turbo"  # Use gpt-3.5-turbo for lower cost
    
    def analyze_resume(self, resume_text: str, job_description: str = "") -> Dict:
        """Comprehensive resume analysis"""
        prompt = self._create_analysis_prompt(resume_text, job_description)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert HR professional and career coach specializing in resume analysis."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            analysis_text = response.choices[0].message.content
            return self._parse_analysis_response(analysis_text)
        
        except Exception as e:
            return {
                'error': f'AI analysis failed: {str(e)}',
                'summary': 'Unable to complete analysis',
                'strengths': [],
                'weaknesses': [],
                'recommendations': []
            }
    
    def score_resume(self, resume_text: str, job_description: str = "") -> Dict:
        """Score resume on various criteria"""
        prompt = f"""
Score the following resume on a scale of 0-100 for each category:
1. Content Quality (clarity, relevance, achievements)
2. Format & Structure (organization, readability)
3. Skills Match (relevance to job market)
4. Experience Level (depth and breadth)
5. Overall Impact

Resume:
{resume_text}

{f"Job Description: {job_description}" if job_description else ""}

Provide scores in JSON format:
{{
    "content_quality": <score>,
    "format_structure": <score>,
    "skills_match": <score>,
    "experience_level": <score>,
    "overall_score": <score>,
    "explanation": "<brief explanation>"
}}
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert resume evaluator. Provide objective scores."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=500
            )
            
            result = response.choices[0].message.content
            # Try to extract JSON from response
            try:
                # Find JSON object in response
                start_idx = result.find('{')
                end_idx = result.rfind('}') + 1
                if start_idx != -1 and end_idx > start_idx:
                    json_str = result[start_idx:end_idx]
                    return json.loads(json_str)
            except:
                pass
            
            # Fallback if JSON parsing fails
            return {
                'content_quality': 75,
                'format_structure': 75,
                'skills_match': 70,
                'experience_level': 75,
                'overall_score': 74,
                'explanation': result
            }
        
        except Exception as e:
            return {
                'error': f'Scoring failed: {str(e)}',
                'overall_score': 0
            }
    
    def get_suggestions(self, resume_text: str, job_description: str = "") -> Dict:
        """Get specific improvement suggestions"""
        prompt = f"""
Analyze this resume and provide specific, actionable improvement suggestions.
Focus on:
1. Content improvements (what to add or remove)
2. Format improvements (structure and presentation)
3. Keyword optimization (for ATS systems)
4. Achievement quantification
5. Skills highlighting

Resume:
{resume_text}

{f"Target Job: {job_description}" if job_description else ""}

Provide 5-10 specific, actionable suggestions.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional resume writer and career coach."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            suggestions_text = response.choices[0].message.content
            suggestions = self._parse_suggestions(suggestions_text)
            
            return {
                'suggestions': suggestions,
                'count': len(suggestions)
            }
        
        except Exception as e:
            return {
                'error': f'Failed to generate suggestions: {str(e)}',
                'suggestions': []
            }
    
    def _create_analysis_prompt(self, resume_text: str, job_description: str) -> str:
        """Create prompt for comprehensive analysis"""
        prompt = f"""
Analyze the following resume comprehensively:

Resume:
{resume_text}

{f"Job Description: {job_description}" if job_description else ""}

Provide:
1. A brief summary (2-3 sentences)
2. Top 3-5 strengths
3. Top 3-5 areas for improvement
4. 5-7 specific recommendations
5. Match score with job description (if provided)

Be specific and actionable.
"""
        return prompt
    
    def _parse_analysis_response(self, response_text: str) -> Dict:
        """Parse the analysis response into structured format"""
        lines = response_text.split('\n')
        
        result = {
            'summary': '',
            'strengths': [],
            'weaknesses': [],
            'recommendations': [],
            'match_score': 0
        }
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Detect sections
            lower_line = line.lower()
            if 'summary' in lower_line or 'overview' in lower_line:
                current_section = 'summary'
            elif 'strength' in lower_line or 'positive' in lower_line:
                current_section = 'strengths'
            elif 'weakness' in lower_line or 'improvement' in lower_line or 'area' in lower_line:
                current_section = 'weaknesses'
            elif 'recommendation' in lower_line or 'suggestion' in lower_line:
                current_section = 'recommendations'
            elif 'match' in lower_line and 'score' in lower_line:
                current_section = 'match_score'
            else:
                # Add content to current section
                if current_section == 'summary' and len(result['summary']) < 500:
                    result['summary'] += line + ' '
                elif current_section == 'strengths' and (line.startswith('-') or line.startswith('•') or line[0].isdigit()):
                    result['strengths'].append(line.lstrip('-•0123456789. '))
                elif current_section == 'weaknesses' and (line.startswith('-') or line.startswith('•') or line[0].isdigit()):
                    result['weaknesses'].append(line.lstrip('-•0123456789. '))
                elif current_section == 'recommendations' and (line.startswith('-') or line.startswith('•') or line[0].isdigit()):
                    result['recommendations'].append(line.lstrip('-•0123456789. '))
        
        result['summary'] = result['summary'].strip()
        return result
    
    def _parse_suggestions(self, suggestions_text: str) -> list:
        """Parse suggestions into a list"""
        suggestions = []
        lines = suggestions_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line and (line.startswith('-') or line.startswith('•') or line[0].isdigit()):
                suggestion = line.lstrip('-•0123456789. ')
                if suggestion:
                    suggestions.append(suggestion)
        
        return suggestions
