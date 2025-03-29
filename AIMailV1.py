import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time
import psswrd
import groq
import os
import ipywidgets as widgets
from IPython.display import display


# Initialize Groq client
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
Groq = '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'
client = groq.Client(api_key=Groq)

# Load email content
# sub = open('subject.txt', "r").read()
# base = open('Body_base2.txt', "r").read()

# Load the CSV file
csv_file = '/Users/vaibhavwadhwa/Self Projects/my data/Beekh/11897085_a44e0c85-214e-4fd4-b77b-7a0162975840.csv'
data = pd.read_csv(csv_file)
data.fillna(0)
data = data.iloc[65:]

# Email credentials
your_email = psswrd.your_email2
your_password = psswrd.your_password2  # Use the App Password generated from Gmail

# Resume file
resume_filename = "Vaibhav_Wadhwa.pdf"

# Setup the server
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(your_email, your_password)
res='''VAIBHAV WADHWA
Male, 21
Mobile: +91-93111-14563 | Email: wadhwa.vaibhav11@gmail.com
________________________________________
EDUCATION
Name of Course	Year	College/School	%	Dept. Rank
B.Tech (Industrial IoT)	2021-2025	Vivekananda Institute of Professional Studies	8.25 CGPA	-
AISSCE (Class XII)	2021	Happy Home Public School, Delhi	86%	-
AISCE (Class X)	2019	Happy Home Public School, Delhi	89%	-
________________________________________
INTERNSHIPS
AI Software Intern, Zummit Infolabs, Delhi (Oct 2023 – Present)
AI-driven solutions provider specializing in generative models and NLP.
•	Developed chatbots using NLP, reducing customer query response time by 30%.
o	Improved operational efficiency by automating repetitive workflows.
•	Collaborated on refining AI architectures, achieving 95% model uptime in production.
Data Analyst, Nikah Forever, Okhla, Delhi (Aug 2024 – Present)
Matrimonial platform leveraging data analytics for user engagement.
•	Built Power BI dashboards tracking KPIs, reducing reporting time by 30%.
o	Increased campaign ROI by 12% through A/B testing implementation.
•	Automated SQL data pipelines, reducing errors by 25%.
________________________________________
ACADEMIC PROJECTS
•	Blood Cancer Detection using CV:
Developed an AI diagnostic tool using deep learning (TensorFlow) to detect cancer from blood smear images with 98% accuracy. Role: Sole developer. Outcome: Shortlisted for 2024 AI Healthcare Innovation Award.
•	Speech Emotion Recognition:
Built an NLP model to classify 10 emotions from 150+ audio samples using MFCC features. Role: Team lead. Outcome: Integrated into a React app for real-time analysis.
________________________________________
ACADEMIC ACHIEVEMENTS AND AWARDS
•	Awarded Best Paper Award at an International Conference for research on AI-driven analysis of Shreemad Bhagwad Geeta (2024).
•	Earned HackerRank Gold Badges for Python, SQL, and Problem Solving (Top 1% globally).
________________________________________
POSITIONS OF RESPONSIBILITY
•	Management Head, Srijan (Eco & Social Outreach Club):
o	Led 15+ donation drives and community programs impacting 2,000+ students.
o	Managed finances, raising ₹5L+ in donations for sustainability initiatives.
•	Management Head, Kavyarang (Literary Club):
o	Organized 7+ literary events and 5+ competitions, increasing club participation by 40%.
o	Strategized outreach campaigns to engage 500+ students across Delhi colleges.
________________________________________
EXTRA-CURRICULAR ACTIVITIES AND ACHIEVEMENTS
•	Won 3+ hackathons for AI projects, including Waste Classification App and Crop Disease Detection.
•	Volunteer, Sachkhand Foundation: Managed technical logistics for 10+ community welfare events.
________________________________________
OTHER INFORMATION
•	Technical Skills: Python, SQL, TensorFlow, Power BI, AWS, Git.
•	Interests: AI research, community service, competitive coding.
•	Languages: English (fluent), Hindi (native).

'''
sample_mail='''Dear Ms. Singh,
My name is Rohan Gupta, and I am interested in learning more about the open associate marketing representative position at your company, Whitehouse Marketing Firm. I reached out to your assistant, Mr. Sharma, who was kind enough to provide me with your email address so I could get in contact with you.
While doing research on various marketing firms in the area, I repeatedly noticed that your firm has received numerous industry accolades over the last decade, perhaps most notably the Best Marketing Agency award for the past four years. I also came across your profile in Digital Media Weekly, where you spoke passionately about your love for this industry and how much you value your team. Your enthusiasm for digital media marketing and appreciation for your associates is exactly what I have been looking for in an employer, and I would love to meet with you to discuss this more.
If you are available, I would love to schedule a time to meet this upcoming week to discuss the position and my own qualifications as a marketing associate. Of course, I have no problem adapting to your availability. Feel free to contact me through this email address and I look forward to hearing from you soon.
Sincerely,
Rohan Gupta'''

def Body(name, company):
    f=str()
    op = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
            "role": "system",
            "content": f"{res}"
        },
        {
            "role": "user",
            "content": f"Write a mail to hr named {name} working at {company}, research about {company} and show them how I can be an asset to their company and talk about my accomplishments and experience.follow this style of mail {sample_mail} Just the body no Preamble."
        }],
        temperature=0.83,
        max_completion_tokens=400,
        top_p=1,
        stream=True,
        stop=None
    )
    for chunk in op:
        f+=f'{chunk.choices[0].delta.content}'
        
    return f

def send_emails():
    for index, row in data.iterrows():
        try:
            recipient_emails = []
            if pd.notna(row['Email']):
                recipient_emails = [email.strip() for email in row['Email'].split(',')]
            elif pd.notna(row['Work email']):
                recipient_emails = [email.strip() for email in row['Work email'].split(',')]
            elif pd.notna(row['Direct email']):
                recipient_emails = [email.strip() for email in row['Direct email'].split(',')]
            elif pd.notna(row['Email']):
                recipient_emails = [email.strip() for email in row['Email'].split(',')]
            else:
                continue

            recipient_email_str = ', '.join(recipient_emails)
            
            # Create a message
            #recipient_name = row["/Users/vaibhavwadhwa/Self Projects/my data/Beekh/11897085_a44e0c85-214e-4fd4-b77b-7a0162975840.csv"]
            recipient_name=row['Name']
            recipient_company = row["Company Name"]
            body = f'''Dear {recipient_name}
{Body(name=recipient_name, company=recipient_company)}

Sincerely,
Vaibhav Wadhwa
+91-93111-14563
'''
            
            # Create the email
            msg = MIMEMultipart()
            msg['From'] = your_email
            msg['To'] = recipient_email_str
            msg['Subject'] = "Application for the position of AI Software Engineer"

            msg.attach(MIMEText(body, 'plain'))

            # Attach the resume
            with open(resume_filename, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename= Vaibhav_Wadhwa.pdf')
                msg.attach(part)

            # Send the email
            server.sendmail(your_email, recipient_emails + ["vwadhwa02@gmail.com"], msg.as_string())
            print(f'Email sent to {recipient_email_str}')
            
            time.sleep(0.5)
        except Exception as e:
            print(f"Failed to send email to {recipient_email_str}: {e}")
            continue

    # Quit the server 
    server.quit()

# # Create a button widget
def main():
    send_emails()
    print("All emails sent successfully")
main()