from faker import Faker
from fpdf import FPDF
import random
import os

ROLES = [
    {
        "title": "Software Engineer",
        "skills": ["Python", "Machine Learning", "REST APIs", "Cloud", "Docker", "Linux"],
        "exp_range": (2, 8)
    },
    {
        "title": "Data Scientist",
        "skills": ["Python", "Pandas", "Numpy", "Deep Learning", "SQL", "Statistics"],
        "exp_range": (1, 6)
    },
    {
        "title": "DevOps Engineer",
        "skills": ["AWS", "Terraform", "CI/CD", "Kubernetes", "Linux", "Python"],
        "exp_range": (3, 10)
    },
    {
        "title": "Frontend Developer",
        "skills": ["JavaScript", "React", "CSS", "HTML", "Redux", "TypeScript"],
        "exp_range": (1, 7)
    }
]

fake = Faker()

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, self.title, ln=True, align='C')
        self.ln(5)

def generate_resume(role, filename):
    pdf = PDF()
    pdf.title = "Resume"
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    name = fake.name()
    pdf.cell(0, 10, name, ln=True)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 8, fake.address().replace('\n', ', '), ln=True)
    pdf.cell(0, 8, fake.email(), ln=True)
    pdf.cell(0, 8, fake.phone_number(), ln=True)
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 8, f"Objective", ln=True)
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 8, f"Seeking a {role['title']} position to utilize my skills in {', '.join(role['skills'][:3])}.")
    pdf.ln(2)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 8, "Skills", ln=True)
    pdf.set_font('Arial', '', 12)
    skills = random.sample(role['skills'], k=random.randint(3, len(role['skills'])))
    pdf.multi_cell(0, 8, ', '.join(skills))
    pdf.ln(2)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 8, "Experience", ln=True)
    pdf.set_font('Arial', '', 12)
    years = random.randint(*role['exp_range'])
    for i in range(random.randint(1, 2)):
        company = fake.company()
        job_title = role['title']
        pdf.cell(0, 8, f"{job_title} at {company} ({fake.year()} - {fake.year()})", ln=True)
        pdf.multi_cell(0, 8, f"Worked on {random.choice(role['skills'])} and contributed to team projects.")
    pdf.ln(2)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 8, "Education", ln=True)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 8, f"{fake.job()} - {fake.company()} ({fake.year()})", ln=True)
    pdf.output(filename)

if __name__ == "__main__":
    os.makedirs("resumes", exist_ok=True)
    for idx, role in enumerate(ROLES):
        for i in range(2):
            filename = f"resumes/{role['title'].replace(' ', '_')}_{i+1}.pdf"
            generate_resume(role, filename)
    print("Sample resumes generated in the 'resumes/' folder.")
