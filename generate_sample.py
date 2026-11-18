import os
from docx import Document

def generate_resume():
    doc = Document()
    doc.add_heading('John Doe - Software Engineer', 0)
    
    doc.add_heading('Summary', level=1)
    doc.add_paragraph(
        'Experienced software engineer with a strong background in web development. '
        'I have a proven track record of problem solving and leadership in team environments. '
        'I have previously worked with jQuery and Hadoop, but now focus on modern stacks.'
    )
    
    doc.add_heading('Skills', level=1)
    skills = ['Python', 'Django', 'React', 'JavaScript', 'Docker', 'AWS', 'SQL', 'Git', 'jQuery', 'Hadoop']
    for skill in skills:
        doc.add_paragraph(skill, style='List Bullet')
        
    doc.add_heading('Experience', level=1)
    doc.add_heading('Senior Developer - TechCorp', level=2)
    doc.add_paragraph(
        'Led a team of 5 developers to build a scalable REST API using Python and Django. '
        'Managed deployments using Docker and AWS. Collaborated with product managers in an Agile environment.'
    )
    
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sample_resume.docx')
    doc.save(output_path)
    print(f"sample_resume.docx created successfully at: {output_path}")

if __name__ == '__main__':
    generate_resume()
