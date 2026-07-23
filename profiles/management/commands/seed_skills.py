from django.core.management.base import BaseCommand
from profiles.models import Skill


SKILLS = [
    # Backend
    ("Python",          "Backend"),
    ("Django",          "Backend"),
    ("Django REST Framework", "Backend"),
    ("FastAPI",         "Backend"),
    ("Node.js",         "Backend"),
    ("Express.js",      "Backend"),
    ("Java",            "Backend"),
    ("Spring Boot",     "Backend"),
    ("Go",              "Backend"),
    ("Ruby on Rails",   "Backend"),
    ("PHP",             "Backend"),
    ("Laravel",         "Backend"),
    ("C#",              "Backend"),
    (".NET",            "Backend"),
    ("PostgreSQL",      "Backend"),
    ("MySQL",           "Backend"),
    ("MongoDB",         "Backend"),
    ("Redis",           "Backend"),
    ("GraphQL",         "Backend"),
    ("REST API",        "Backend"),

    # Frontend
    ("React",           "Frontend"),
    ("Next.js",         "Frontend"),
    ("Vue.js",          "Frontend"),
    ("Angular",         "Frontend"),
    ("TypeScript",      "Frontend"),
    ("JavaScript",      "Frontend"),
    ("HTML",            "Frontend"),
    ("CSS",             "Frontend"),
    ("Tailwind CSS",    "Frontend"),
    ("Bootstrap",       "Frontend"),
    ("Svelte",          "Frontend"),
    ("Redux",           "Frontend"),

    # Mobile
    ("React Native",    "Mobile"),
    ("Flutter",         "Mobile"),
    ("Kotlin",          "Mobile"),
    ("Swift",           "Mobile"),
    ("Android",         "Mobile"),
    ("iOS",             "Mobile"),

    # DevOps / Cloud
    ("Docker",          "DevOps"),
    ("Kubernetes",      "DevOps"),
    ("AWS",             "DevOps"),
    ("Google Cloud",    "DevOps"),
    ("Azure",           "DevOps"),
    ("CI/CD",           "DevOps"),
    ("Linux",           "DevOps"),
    ("Nginx",           "DevOps"),
    ("Terraform",       "DevOps"),
    ("GitHub Actions",  "DevOps"),

    # Data Science / AI
    ("Machine Learning","Data Science"),
    ("Deep Learning",   "Data Science"),
    ("TensorFlow",      "Data Science"),
    ("PyTorch",         "Data Science"),
    ("Data Analysis",   "Data Science"),
    ("Pandas",          "Data Science"),
    ("NumPy",           "Data Science"),
    ("Scikit-learn",    "Data Science"),
    ("Computer Vision", "Data Science"),
    ("NLP",             "Data Science"),
    ("LLM",             "Data Science"),

    # Design
    ("UI/UX Design",    "Design"),
    ("Figma",           "Design"),
    ("Adobe XD",        "Design"),
    ("Graphic Design",  "Design"),
    ("Illustrator",     "Design"),
    ("Photoshop",       "Design"),
    ("Motion Design",   "Design"),
    ("Canva",           "Design"),
    ("Prototyping",     "Design"),

    # Other
    ("Git",             "Other"),
    ("Agile",           "Other"),
    ("Scrum",           "Other"),
    ("Technical Writing","Other"),
    ("Blockchain",      "Other"),
    ("Web3",            "Other"),
    ("Solidity",        "Other"),
    ("Cybersecurity",   "Other"),
    ("QA Testing",      "Other"),
    ("Selenium",        "Other"),
]


class Command(BaseCommand):
    help = 'Seed the Skill table with common tech skills'

    def handle(self, *args, **kwargs):
        created = 0
        skipped = 0

        for name, category in SKILLS:
            obj, was_created = Skill.objects.get_or_create(
                name=name,
                defaults={'category': category}
            )
            if was_created:
                created += 1
            else:
                skipped += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Done. {created} skills created, {skipped} already existed.'
            )
        )