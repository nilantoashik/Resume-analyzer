from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

c = canvas.Canvas("test_resume.pdf", pagesize=letter)
c.drawString(100, 750, "John Doe")
c.drawString(100, 730, "john@email.com | 123-456-7890")
c.drawString(100, 700, "EXPERIENCE")
c.drawString(100, 680, "Software Engineer at Tech Corp")
c.drawString(100, 660, "Developed Python applications using Flask and JavaScript")
c.drawString(100, 630, "SKILLS")
c.drawString(100, 610, "Python, JavaScript, React, Flask, SQL, Git")
c.save()

print("PDF created successfully: test_resume.pdf")
