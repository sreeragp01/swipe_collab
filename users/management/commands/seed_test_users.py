from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from profiles.models import Skill, FreelancerProfile, CompanyProfile

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed test users for swipe testing'

    def handle(self, *args, **kwargs):

        # ── Freelancers ───────────────────────────────
        freelancers = [
            {
                'email': 'alex@test.com',
                'username': 'alex_dev',
                'name': 'Alex Johnson',
                'bio': 'Full stack developer with 4 years of experience in Django and React.',
                'experience_years': 4,
                'availability': 'full_time',
                'city': 'Bangalore',
                'country': 'India',
                'skills': ['Python', 'Django', 'React', 'PostgreSQL'],
            },
            {
                'email': 'priya@test.com',
                'username': 'priya_ui',
                'name': 'Priya Sharma',
                'bio': 'UI/UX designer passionate about creating intuitive digital experiences.',
                'experience_years': 3,
                'availability': 'part_time',
                'city': 'Mumbai',
                'country': 'India',
                'skills': ['UI/UX Design', 'Figma', 'Adobe XD', 'Prototyping'],
            },
            {
                'email': 'rahul@test.com',
                'username': 'rahul_ml',
                'name': 'Rahul Nair',
                'bio': 'Machine learning engineer focused on NLP and computer vision.',
                'experience_years': 5,
                'availability': 'contract',
                'city': 'Hyderabad',
                'country': 'India',
                'skills': ['Python', 'Machine Learning', 'TensorFlow', 'NLP'],
            },
            {
                'email': 'sara@test.com',
                'username': 'sara_mobile',
                'name': 'Sara Thomas',
                'bio': 'Mobile developer building cross-platform apps with Flutter.',
                'experience_years': 2,
                'availability': 'full_time',
                'city': 'Kochi',
                'country': 'India',
                'skills': ['Flutter', 'React Native', 'Kotlin', 'Firebase'],
            },
            {
                'email': 'arjun@test.com',
                'username': 'arjun_devops',
                'name': 'Arjun Menon',
                'bio': 'DevOps engineer specializing in cloud infrastructure and CI/CD pipelines.',
                'experience_years': 6,
                'availability': 'full_time',
                'city': 'Pune',
                'country': 'India',
                'skills': ['Docker', 'Kubernetes', 'AWS', 'CI/CD'],
            },
        ]

        # ── Companies ─────────────────────────────────
        companies = [
            {
                'email': 'techcorp@test.com',
                'username': 'techcorp',
                'name': 'TechCorp India',
                'description': 'We build SaaS products for the Indian market. Looking for talented developers.',
                'city': 'Bangalore',
                'country': 'India',
                'skills': ['Python', 'Django', 'React', 'PostgreSQL'],
            },
            {
                'email': 'designstudio@test.com',
                'username': 'designstudio',
                'name': 'DesignStudio',
                'description': 'Creative agency specializing in mobile app design and brand identity.',
                'city': 'Mumbai',
                'country': 'India',
                'skills': ['UI/UX Design', 'Figma', 'Prototyping'],
            },
            {
                'email': 'ailab@test.com',
                'username': 'ailab',
                'name': 'AI Lab',
                'description': 'AI startup building intelligent tools for healthcare and education.',
                'city': 'Hyderabad',
                'country': 'India',
                'skills': ['Machine Learning', 'Python', 'TensorFlow', 'NLP'],
            },
        ]

        created_count = 0

        # Create freelancers
        for data in freelancers:
            if User.objects.filter(email=data['email']).exists():
                self.stdout.write(f"  Skipping {data['email']} — already exists")
                continue

            user = User.objects.create_user(
                email=data['email'],
                username=data['username'],
                password='Test@1234',
                role=User.ROLE_FREELANCER,
                is_verified=True,
                face_verified=True,
                is_paid=True,
                is_active=True,
            )

            skills = Skill.objects.filter(name__in=data['skills'])
            profile = FreelancerProfile.objects.create(
                user=user,
                name=data['name'],
                bio=data['bio'],
                experience_years=data['experience_years'],
                availability=data['availability'],
                city=data['city'],
                country=data['country'],
            )
            profile.skills.set(skills)

            self.stdout.write(self.style.SUCCESS(f"  ✓ Freelancer: {data['email']}"))
            created_count += 1

        # Create companies
        for data in companies:
            if User.objects.filter(email=data['email']).exists():
                self.stdout.write(f"  Skipping {data['email']} — already exists")
                continue

            user = User.objects.create_user(
                email=data['email'],
                username=data['username'],
                password='Test@1234',
                role=User.ROLE_COMPANY,
                is_verified=True,
                face_verified=True,
                is_paid=True,
                is_active=True,
            )

            skills = Skill.objects.filter(name__in=data['skills'])
            profile = CompanyProfile.objects.create(
                user=user,
                name=data['name'],
                description=data['description'],
                city=data['city'],
                country=data['country'],
            )
            profile.skills.set(skills)

            self.stdout.write(self.style.SUCCESS(f"  ✓ Company: {data['email']}"))
            created_count += 1

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(
            f'Done! {created_count} test users created.'
        ))
        self.stdout.write('')
        self.stdout.write('Login credentials for all test users:')
        self.stdout.write('  Password: Test@1234')
        self.stdout.write('')
        self.stdout.write('Freelancers:')
        for f in freelancers:
            self.stdout.write(f"  {f['email']}")
        self.stdout.write('')
        self.stdout.write('Companies:')
        for c in companies:
            self.stdout.write(f"  {c['email']}")