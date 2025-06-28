from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, self.title, ln=True, align='C')
        self.ln(5)

def generate_high_score_resume(name, filename):
    pdf = PDF()
    pdf.title = "Resume"
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, name, ln=True)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 8, "123 Main St, Anytown, USA", ln=True)
    pdf.cell(0, 8, f"{name.lower().replace(' ', '.')}@example.com", ln=True)
    pdf.cell(0, 8, "+1-555-123-4567", ln=True)
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 8, f"Objective", ln=True)
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 8, "Seeking a Software Engineer position to utilize my skills in Python, machine learning, and cloud infrastructure.")
    pdf.ln(2)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 8, "Skills", ln=True)
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 8, "Python, Machine Learning, REST APIs, Cloud (AWS/GCP), Docker, Linux, Problem Solving")
    pdf.ln(2)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 8, "Experience", ln=True)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 8, "Software Engineer at TechCorp (2021-2025)", ln=True)
    pdf.multi_cell(0, 8, "Developed and deployed machine learning models using Python on AWS. Built REST APIs for data services. Led cloud migration projects. Solved complex technical problems.")
    pdf.cell(0, 8, "Software Engineer at DataCloud (2018-2021)", ln=True)
    pdf.multi_cell(0, 8, "Led a team to migrate legacy systems to cloud infrastructure. Designed and implemented scalable REST APIs.")
    pdf.ln(2)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 8, "Education", ln=True)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 8, "B.Sc. Computer Science - MIT (2018)", ln=True)
    pdf.output(filename)

if __name__ == "__main__":
    os.makedirs("resumes", exist_ok=True)
    generate_high_score_resume("Jane Doe", "resumes/Software_Engineer_HighScore1.pdf")
    generate_high_score_resume("John Smith", "resumes/Software_Engineer_HighScore2.pdf")
    print("High-scoring resumes generated in the 'resumes/' folder.")
