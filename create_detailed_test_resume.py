from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_detailed_test_resume():
    """Create a more detailed test resume PDF"""
    pdf_path = "test_detailed_resume.pdf"
    c = canvas.Canvas(pdf_path, pagesize=letter)
    
    # Add content with proper work experience
    y_position = 750
    
    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, y_position, "SARAH JOHNSON")
    y_position -= 20
    
    c.setFont("Helvetica", 10)
    c.drawString(100, y_position, "sarah.johnson@email.com | (555) 123-4567 | linkedin.com/in/sarahjohnson")
    y_position -= 30
    
    # Professional Summary
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, y_position, "PROFESSIONAL SUMMARY")
    y_position -= 15
    c.setFont("Helvetica", 10)
    c.drawString(100, y_position, "Results-driven Software Engineer with 5+ years of experience building scalable web applications")
    y_position -= 12
    c.drawString(100, y_position, "and cloud infrastructure. Expertise in Python, JavaScript, AWS, and microservices architecture.")
    y_position -= 30
    
    # Professional Experience
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, y_position, "PROFESSIONAL EXPERIENCE")
    y_position -= 20
    
    # Job 1
    c.setFont("Helvetica-Bold", 11)
    c.drawString(100, y_position, "Senior Software Engineer | Tech Solutions Inc.")
    y_position -= 12
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(100, y_position, "June 2021 - Present")
    y_position -= 15
    c.setFont("Helvetica", 9)
    c.drawString(100, y_position, "\u2022 Developed and deployed 15+ microservices using Python, Flask, and Docker reducing latency by 40%")
    y_position -= 12
    c.drawString(100, y_position, "\u2022 Led team of 5 engineers to migrate legacy systems to AWS cloud infrastructure")
    y_position -= 12
    c.drawString(100, y_position, "\u2022 Implemented CI/CD pipelines with Jenkins, improving deployment frequency by 300%")
    y_position -= 12
    c.drawString(100, y_position, "\u2022 Optimized database queries in PostgreSQL, reducing query time by 60%")
    y_position -= 12
    c.drawString(100, y_position, "\u2022 Mentored 3 junior developers, improving team productivity by 25%")
    y_position -= 25
    
    # Job 2
    c.setFont("Helvetica-Bold", 11)
    c.drawString(100, y_position, "Software Engineer | Digital Innovations Corp.")
    y_position -= 12
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(100, y_position, "January 2019 - May 2021")
    y_position -= 15
    c.setFont("Helvetica", 9)
    c.drawString(100, y_position, "\u2022 Built RESTful APIs serving 100K+ daily active users with 99.9% uptime")
    y_position -= 12
    c.drawString(100, y_position, "\u2022 Collaborated with cross-functional teams using Agile/Scrum methodologies")
    y_position -= 12
    c.drawString(100, y_position, "\u2022 Developed React-based dashboards for real-time data visualization")
    y_position -= 12
    c.drawString(100, y_position, "\u2022 Reduced API response time by 50% through caching implementation with Redis")
    y_position -= 25
    
    # Job 3
    c.setFont("Helvetica-Bold", 11)
    c.drawString(100, y_position, "Junior Developer | StartupXYZ Technologies")
    y_position -= 12
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(100, y_position, "June 2018 - December 2018")
    y_position -= 15
    c.setFont("Helvetica", 9)
    c.drawString(100, y_position, "\u2022 Assisted in building web applications using Django and JavaScript")
    y_position -= 12
    c.drawString(100, y_position, "\u2022 Participated in code reviews and contributed to team best practices")
    y_position -= 12
    c.drawString(100, y_position, "\u2022 Fixed 50+ bugs improving application stability")
    y_position -= 30
    
    # Education
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, y_position, "EDUCATION")
    y_position -= 15
    c.setFont("Helvetica", 10)
    c.drawString(100, y_position, "Bachelor of Science in Computer Science")
    y_position -= 12
    c.drawString(100, y_position, "University of Technology | Graduated: May 2018 | GPA: 3.8/4.0")
    y_position -= 25
    
    # Skills
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, y_position, "TECHNICAL SKILLS")
    y_position -= 15
    c.setFont("Helvetica", 10)
    c.drawString(100, y_position, "Languages: Python, JavaScript, TypeScript, SQL")
    y_position -= 12
    c.drawString(100, y_position, "Frameworks: Flask, Django, React, Node.js, Express")
    y_position -= 12
    c.drawString(100, y_position, "Cloud & DevOps: AWS (EC2, S3, Lambda), Docker, Kubernetes, Jenkins, CI/CD")
    y_position -= 12
    c.drawString(100, y_position, "Databases: PostgreSQL, MongoDB, Redis, MySQL")
    y_position -= 25
    
    # Certifications
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, y_position, "CERTIFICATIONS")
    y_position -= 15
    c.setFont("Helvetica", 10)
    c.drawString(100, y_position, "\u2022 AWS Certified Solutions Architect - Associate (2023)")
    y_position -= 12
    c.drawString(100, y_position, "\u2022 Certified Scrum Master (CSM) (2022)")
    
    c.save()
    print(f"Created detailed test resume: {pdf_path}")
    return pdf_path

if __name__ == "__main__":
    create_detailed_test_resume()
