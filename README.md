```python
from typing import List, Dict, TypedDict

class ContactInfo(TypedDict):
    email: str
    github: str
    linkedin: str

class Skill(TypedDict):
    name: str
    proficiency: str

class Experience(TypedDict):
    role: str
    company: str
    start_date: str
    end_date: str
    responsibilities: List[str]

class EducationDetail(TypedDict):
    degree: str
    institution: str
    additional_info: str

class Certification(TypedDict):
    name: str

class Resume(TypedDict):
    name: str
    contact: ContactInfo
    objective: str
    experiences: List[Experience]
    skills: List[Skill]
    education: List[EducationDetail]
    certifications: List[Certification]

def create_resume() -> Resume:
    return {
        "name": "Don Johnson",
        "contact": {
            "email": "dj@codetestcode.io",
            "github": "github.com/copyleftdev",
            "linkedin": "linkedin.com/in/donscv"
        },
        "objective": ("Seasoned technology professional with over 16 years of experience "
                      "in Quality Engineering, DevOps, and Site Reliability Engineering roles, "
                      "seeking to advance career as a Senior Software Quality Automation Engineer. "
                      "Adept at enhancing product quality through innovative testing strategies and "
                      "proficient in Agile and SAFe environments."),
        "experiences": [
            {
                "role": "Senior Automation Engineer",
                "company": "Zuub",
                "start_date": "January 2023",
                "end_date": "Present",
                "responsibilities": [
                    "Developed and deployed advanced automation frameworks that enhance the security and efficiency of Zuub’s real-time dental insurance verification software, ensuring compliance with SOC and HIPAA standards.",
                    "Led the integration of automated testing processes that ensure the reliability and functionality of digital treatment plans.",
                    "Innovated testing strategies for Zuub’s integrated billing software, improving the patient billing experience by facilitating smarter, online payments."
                ]
            },
            # Additional experiences can be added here
        ],
        "skills": [
            {"name": "Testing", "proficiency": "Expert in API, UI, Performance, Security, Regression, and Automation Testing"},
            {"name": "Programming", "proficiency": "Proficient in JavaScript, Python, Go, C#, Kotlin, Java, TypeScript, SQL"},
            {"name": "Tools", "proficiency": "Jenkins, Postman, JMeter, GitHub Actions, Selenium, Cypress, Playwright"},
            {"name": "Systems", "proficiency": "Proficient with Docker, AWS, GCP; Windows, Linux, macOS"},
            {"name": "Methodologies", "proficiency": "Agile, Scrum, SAFe, Continuous Integration/Deployment"}
        ],
        "education": [
            {"degree": "High School Diploma", "institution": "", "additional_info": ""},
            {"degree": "Continuing Education Courses", "institution": "Pasadena City College", "additional_info": ""}
        ],
        "certifications": [
            {"name": "Certified Scrum Master"}
        ]
    }

resume = create_resume()
print(resume)

```


[![copyleftdev GitHub stats](https://github-readme-stats.vercel.app/api?username=copyleftdev)](https://github.com/copyleftdev/github-readme-stats)

# Grey Beard Trophies

[![trophy](https://github-profile-trophy.vercel.app/?username=copyleftdev)](https://github.com/copyleftdev/github-profile-trophy)

# Languages and Tools I  Enjoy

[![My Skills](https://skillicons.dev/icons?i=py,rust,go,aws,gcp,bash,docker,fastapi,firebase,git,obsidian,cypress,githubactions,htmx,postgres,rabbitmq,redis,terraform,ts,zig)](https://skillicons.dev)

<a href="https://gitroll.io/profile/uB8fjxzB4NHUkjkK1pggNJbWLqz93" target="_blank"><img src="https://gitroll.io/api/badges/profiles/v1/uB8fjxzB4NHUkjkK1pggNJbWLqz93" alt="GitRoll Profile Badge"/></a>
