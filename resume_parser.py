import re
import PyPDF2
from docx import Document
from typing import Dict, List

class ResumeParser:
    """Parser for extracting and analyzing resume content"""
    
    def extract_text(self, filepath: str) -> str:
        """Extract text from resume file (PDF or DOCX)"""
        if filepath.endswith('.pdf'):
            return self._extract_from_pdf(filepath)
        elif filepath.endswith('.docx') or filepath.endswith('.doc'):
            return self._extract_from_docx(filepath)
        else:
            raise ValueError("Unsupported file format")
    
    def _extract_from_pdf(self, filepath: str) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            with open(filepath, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
        return text
    
    def _extract_from_docx(self, filepath: str) -> str:
        """Extract text from DOCX file"""
        text = ""
        try:
            doc = Document(filepath)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            raise Exception(f"Error reading DOCX: {str(e)}")
        return text
    
    def parse_resume(self, text: str) -> Dict:
        """Parse resume text and extract structured data"""
        return {
            'email': self._extract_email(text),
            'phone': self._extract_phone(text),
            'skills': self._extract_skills(text),
            'experience_years': self._estimate_experience_years(text),
            'education': self._extract_education(text),
            'work_experience': self._extract_work_experience(text),
            'full_text': text
        }
    
    def _extract_email(self, text: str) -> str:
        """Extract email address from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        matches = re.findall(email_pattern, text)
        return matches[0] if matches else ""
    
    def _extract_phone(self, text: str) -> str:
        """Extract phone number from text"""
        # Match various phone number formats
        phone_patterns = [
            r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\d{10}'
        ]
        
        for pattern in phone_patterns:
            matches = re.findall(pattern, text)
            if matches:
                return matches[0]
        return ""
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills from text"""
        # Common technical skills to look for
        common_skills = [
            'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift',
            'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'spring',
            'sql', 'mongodb', 'postgresql', 'mysql', 'redis',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes',
            'git', 'jenkins', 'ci/cd', 'agile', 'scrum',
            'machine learning', 'deep learning', 'ai', 'data science',
            'html', 'css', 'typescript', 'rest api', 'graphql',
            'tensorflow', 'pytorch', 'pandas', 'numpy',
            'leadership', 'communication', 'problem solving', 'teamwork'
        ]
        
        text_lower = text.lower()
        found_skills = []
        
        for skill in common_skills:
            if skill in text_lower:
                found_skills.append(skill.title())
        
        return list(set(found_skills))
    
    def _estimate_experience_years(self, text: str) -> int:
        """Estimate years of experience from text"""
        # Look for patterns like "5 years of experience" or "5+ years"
        patterns = [
            r'(\d+)\+?\s*years?\s+(?:of\s+)?experience',
            r'experience[:\s]+(\d+)\+?\s*years?'
        ]
        
        years = []
        for pattern in patterns:
            matches = re.findall(pattern, text.lower())
            years.extend([int(m) for m in matches])
        
        # Return the maximum found, or try to count job positions
        if years:
            return max(years)
        
        # Count years mentioned in dates (rough estimate)
        year_pattern = r'\b(19|20)\d{2}\b'
        year_matches = re.findall(year_pattern, text)
        if len(year_matches) >= 2:
            years_found = [int(y) for y in year_matches]
            return max(years_found) - min(years_found)
        
        return 0
    
    def _extract_education(self, text: str) -> List[str]:
        """Extract education information"""
        education_keywords = [
            'bachelor', 'master', 'phd', 'doctorate', 'associate',
            'b.s.', 'b.a.', 'm.s.', 'm.a.', 'mba', 'ph.d.',
            'degree', 'university', 'college', 'institute'
        ]
        
        education = []
        lines = text.split('\n')
        text_lower = text.lower()
        
        for keyword in education_keywords:
            if keyword in text_lower:
                # Find the line containing the keyword
                for line in lines:
                    if keyword in line.lower() and line.strip():
                        education.append(line.strip())
        
        return list(set(education))[:5]  # Return up to 5 unique entries
    
    def _extract_work_experience(self, text: str) -> List[Dict]:
        """Extract detailed work experience information"""
        experiences = []
        lines = text.split('\n')
        text_lower = text.lower()
        
        # Common job titles to look for
        job_titles = [
            'engineer', 'developer', 'manager', 'analyst', 'consultant',
            'designer', 'architect', 'director', 'lead', 'senior',
            'junior', 'intern', 'specialist', 'coordinator', 'associate',
            'administrator', 'officer', 'executive', 'supervisor', 'technician',
            'scientist', 'researcher', 'programmer', 'administrator'
        ]
        
        # Look for company indicators
        company_keywords = ['inc.', 'corp.', 'llc', 'ltd', 'company', 'technologies', 'systems', 'solutions']
        
        # Extract date ranges - enhanced to handle various formats
        # Matches: "2020 - 2023", "01/2020 - 12/2023", "June 2020 - Present", "Jan 2020 - Dec 2023"
        date_pattern = r'((?:jan|january|feb|february|mar|march|apr|april|may|june|jul|july|aug|august|sep|september|oct|october|nov|november|dec|december)\s+\d{4}|\d{1,2}/\d{4}|\d{4})\s*[-–—]\s*((?:jan|january|feb|february|mar|march|apr|april|may|june|jul|july|aug|august|sep|september|oct|october|nov|november|dec|december)\s+\d{4}|\d{1,2}/\d{4}|\d{4}|present|current)'
        date_matches = list(re.finditer(date_pattern, text, re.IGNORECASE))
        
        # Extract job entries
        for i, line in enumerate(lines):
            line_lower = line.lower().strip()
            if not line_lower or len(line_lower) < 5:
                continue
            
            # Check if line contains a job title
            has_title = any(title in line_lower for title in job_titles)
            
            # Check if line contains company indicators or pipe separator (common in resumes)
            has_company = any(keyword in line_lower for keyword in company_keywords) or '|' in line
            
            # Check if this section contains experience keywords
            context_start = max(0, i - 5)
            context_end = min(len(lines), i + 10)
            context = ' '.join(lines[context_start:context_end]).lower()
            in_experience_section = any(keyword in context for keyword in ['experience', 'employment', 'work history', 'career', 'professional'])
            
            if (has_title or has_company) and in_experience_section:
                # Try to find associated date range
                date_range = None
                duration = None
                
                # First check the next line for date
                if i + 1 < len(lines):
                    next_line = lines[i + 1]
                    date_match_next = re.search(date_pattern, next_line, re.IGNORECASE)
                    if date_match_next:
                        date_range = date_match_next.group()
                        # Calculate duration
                        start_part = date_match_next.group(1).lower()
                        end_part = date_match_next.group(2).lower()
                        
                        # Extract years
                        start_year_match = re.search(r'(\d{4})', start_part)
                        if 'present' in end_part or 'current' in end_part:
                            end_year = 2026
                        else:
                            end_year_match = re.search(r'(\d{4})', end_part)
                            end_year = int(end_year_match.group(1)) if end_year_match else None
                        
                        if start_year_match and end_year:
                            duration = end_year - int(start_year_match.group(1))
                
                # Count bullet points in next few lines
                bullet_count = 0
                for j in range(i + 1, min(i + 15, len(lines))):
                    if any(bullet in lines[j] for bullet in ['•', '●', '◦', '-', '*', '\u2022']):
                        bullet_count += 1
                    elif lines[j].strip() and len(lines[j].strip()) > 10:
                        # Check if this is another job entry
                        if any(title in lines[j].lower() for title in job_titles) and any(keyword in lines[j].lower() for keyword in ['|'] + company_keywords):
                            break  # Next job entry
                
                experiences.append({
                    'title_line': line.strip(),
                    'date_range': date_range,
                    'duration_years': duration,
                    'bullet_points': bullet_count
                })
        
        return experiences
        
        return experiences
