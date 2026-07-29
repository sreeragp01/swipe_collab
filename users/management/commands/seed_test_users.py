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
                'bio': 'DevOps engineer specializing in cloud infrastructure, Kubernetes, and CI/CD automation pipelines.',
                'experience_years': 6,
                'availability': 'full_time',
                'city': 'Pune',
                'country': 'India',
                'skills': ['Docker', 'Kubernetes', 'AWS', 'CI/CD'],
                'portfolio_url': 'https://arjunmenon.dev',
                'github_url': 'https://github.com/arjun-devops',
                'linkedin_url': 'https://linkedin.com/in/arjun-menon-dev',
            },
            {
                'email': 'neha@test.com',
                'username': 'neha_frontend',
                'name': 'Neha Gupta',
                'bio': 'Senior Frontend Developer specializing in React, Next.js, and high-performance Web UI architecture.',
                'experience_years': 5,
                'availability': 'full_time',
                'city': 'Delhi',
                'country': 'India',
                'skills': ['React', 'Next.js', 'TypeScript', 'TailwindCSS'],
                'portfolio_url': 'https://nehagupta.design',
                'github_url': 'https://github.com/neha-frontend',
                'linkedin_url': 'https://linkedin.com/in/neha-gupta-ui',
            },
            {
                'email': 'vikram@test.com',
                'username': 'vikram_cyber',
                'name': 'Vikram Singh',
                'bio': 'Ethical hacker and cybersecurity consultant conducting penetration testing and secure API auditing.',
                'experience_years': 7,
                'availability': 'contract',
                'city': 'Chennai',
                'country': 'India',
                'skills': ['Cybersecurity', 'Penetration Testing', 'Python', 'Docker'],
                'portfolio_url': 'https://vikramsec.io',
                'github_url': 'https://github.com/vikram-cyber',
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
            {
                'email': 'cybernet@test.com',
                'username': 'cybernet',
                'name': 'CyberShield Solutions',
                'description': 'Enterprise cybersecurity and vulnerability assessment firm for fintech and cloud applications.',
                'city': 'Chennai',
                'country': 'India',
                'skills': ['Cybersecurity', 'Penetration Testing', 'Docker', 'Python'],
            },
            {
                'email': 'cloudscale@test.com',
                'username': 'cloudscale',
                'name': 'CloudScale Labs',
                'description': 'High-performance cloud infrastructure engineering and distributed backend microservices.',
                'city': 'Delhi',
                'country': 'India',
                'skills': ['Kubernetes', 'Docker', 'AWS', 'Python', 'Django'],
            },
        ]

        created_count = 0

        # Create companies & projects
        company_projects = {
            'techcorp@test.com': [
                {
                    'title': 'SaaS Platform Backend & Frontend',
                    'description': 'Building a scalable multi-tenant SaaS platform using Django REST framework and React dashboard.',
                    'budget_min': 25000,
                    'budget_max': 50000,
                    'duration': '3_6_months',
                    'skills': ['Python', 'Django', 'React', 'PostgreSQL'],
                },
                {
                    'title': 'Payment Gateway Integration',
                    'description': 'Integrate Razorpay and Stripe payment flows into our backend web app.',
                    'budget_min': 10000,
                    'budget_max': 20000,
                    'duration': 'less_1_month',
                    'skills': ['Django', 'Python', 'PostgreSQL'],
                },
            ],
            'designstudio@test.com': [
                {
                    'title': 'Fintech Mobile App UI/UX Redesign',
                    'description': 'Need an experienced designer to create modern, responsive Figma wireframes and interactive prototypes.',
                    'budget_min': 15000,
                    'budget_max': 30000,
                    'duration': '1_3_months',
                    'skills': ['UI/UX Design', 'Figma', 'Prototyping'],
                },
            ],
            'ailab@test.com': [
                {
                    'title': 'Clinical NLP & Healthcare AI Model',
                    'description': 'Train transformer and NLP models to summarize medical reports accurately and safely.',
                    'budget_min': 35000,
                    'budget_max': 70000,
                    'duration': '3_6_months',
                    'skills': ['Machine Learning', 'Python', 'TensorFlow', 'NLP'],
                },
            ],
            'cybernet@test.com': [
                {
                    'title': 'Penetration Testing & Security Audit',
                    'description': 'Conduct comprehensive security auditing, OWASP vulnerability scans, and API penetration tests.',
                    'budget_min': 30000,
                    'budget_max': 60000,
                    'duration': '1_3_months',
                    'skills': ['Cybersecurity', 'Penetration Testing', 'Python'],
                },
            ],
            'cloudscale@test.com': [
                {
                    'title': 'Kubernetes Cluster Migration & CI/CD Pipeline',
                    'description': 'Migrate AWS EC2 instances to automated Kubernetes clusters with GitHub Actions CI/CD.',
                    'budget_min': 40000,
                    'budget_max': 80000,
                    'duration': '3_6_months',
                    'skills': ['Kubernetes', 'Docker', 'AWS', 'CI/CD'],
                },
            ],
        }

        # Create freelancers
        for data in freelancers:
            user, u_created = User.objects.get_or_create(
                email=data['email'],
                defaults={
                    'username': data['username'],
                    'role': User.ROLE_FREELANCER,
                    'is_verified': True,
                    'face_verified': True,
                    'is_paid': True,
                    'is_active': True,
                }
            )
            if u_created:
                user.set_password('Test@1234')
                user.save()

            profile, _ = FreelancerProfile.objects.get_or_create(
                user=user,
                defaults={
                    'name': data['name'],
                    'bio': data['bio'],
                    'experience_years': data['experience_years'],
                    'availability': data['availability'],
                    'city': data['city'],
                    'country': data['country'],
                    'portfolio_url': data.get('portfolio_url', ''),
                    'github_url': data.get('github_url', ''),
                    'linkedin_url': data.get('linkedin_url', ''),
                }
            )
            if data.get('portfolio_url'):
                profile.portfolio_url = data['portfolio_url']
            if data.get('github_url'):
                profile.github_url = data['github_url']
            if data.get('linkedin_url'):
                profile.linkedin_url = data['linkedin_url']
            profile.save()
            skills = []
            for s_name in data['skills']:
                sk, _ = Skill.objects.get_or_create(name=s_name, defaults={'category': 'General'})
                skills.append(sk)
            profile.skills.set(skills)

            self.stdout.write(self.style.SUCCESS(f"  [OK] Freelancer: {data['email']}"))
            created_count += 1

        # Create companies
        for data in companies:
            user, u_created = User.objects.get_or_create(
                email=data['email'],
                defaults={
                    'username': data['username'],
                    'role': User.ROLE_COMPANY,
                    'is_verified': True,
                    'face_verified': True,
                    'is_paid': True,
                    'is_active': True,
                }
            )
            if u_created:
                user.set_password('Test@1234')
                user.save()

            profile, _ = CompanyProfile.objects.get_or_create(
                user=user,
                defaults={
                    'name': data['name'],
                    'description': data['description'],
                    'city': data['city'],
                    'country': data['country'],
                }
            )
            skills = []
            for s_name in data['skills']:
                sk, _ = Skill.objects.get_or_create(name=s_name, defaults={'category': 'General'})
                skills.append(sk)
            profile.skills.set(skills)

            # Add projects for company
            from projects.models import Project
            p_list = company_projects.get(data['email'], [])
            for p_data in p_list:
                proj, p_created = Project.objects.get_or_create(
                    company=profile,
                    title=p_data['title'],
                    defaults={
                        'description': p_data['description'],
                        'budget_min': p_data['budget_min'],
                        'budget_max': p_data['budget_max'],
                        'duration': p_data['duration'],
                        'status': Project.STATUS_OPEN,
                    }
                )
                p_skills = []
                for s_name in p_data['skills']:
                    sk, _ = Skill.objects.get_or_create(name=s_name, defaults={'category': 'General'})
                    p_skills.append(sk)
                proj.skills.set(p_skills)

            self.stdout.write(self.style.SUCCESS(f"  [OK] Company: {data['email']} (with {len(p_list)} projects)"))
            created_count += 1

        # Seed Portfolio Items for Arjun (arjun@test.com)
        from profiles.models import PortfolioItem
        try:
            arjun_profile = FreelancerProfile.objects.get(user__email='arjun@test.com')
            # 1. Video showcase
            pi1, _ = PortfolioItem.objects.get_or_create(
                freelancer=arjun_profile,
                title='AI Automated Code Reviewer & CI/CD Pipeline',
                defaults={
                    'description': 'Built an intelligent AI agent system that inspects pull requests, runs unit tests, and posts automated code improvements directly to GitHub.',
                    'experience_gained': 'Mastered LangChain, Python AsyncIO, Docker Containers, and GitHub Actions API.',
                    'project_url': 'https://github.com/arjun/ai-code-reviewer',
                    'media_file': 'portfolio_media/demo_video.mp4',
                }
            )
            pi1.media_file = 'portfolio_media/demo_video.mp4'
            pi1.save()

            # 2. Photo showcase
            pi2, _ = PortfolioItem.objects.get_or_create(
                freelancer=arjun_profile,
                title='Real-Time Cloud Analytics Dashboard',
                defaults={
                    'description': 'Designed and built a sleek dark-mode financial & cloud analytics dashboard with dynamic graphs, instant metrics, and security alerting.',
                    'experience_gained': 'Deep expertise in React, WebSockets, Kubernetes monitoring, and Stripe API integration.',
                    'project_url': 'https://github.com/arjun/fintech-dashboard',
                    'media_file': 'portfolio_media/dashboard_photo.png',
                }
            )
            pi2.media_file = 'portfolio_media/dashboard_photo.png'
            pi2.save()

            self.stdout.write(self.style.SUCCESS("  [OK] Seeded sample work showcase items for Arjun (video & photo media attached)"))
        except FreelancerProfile.DoesNotExist:
            pass

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(
            f'Done! Test users and projects created/updated.'
        ))
        self.stdout.write('')
        self.stdout.write('Login credentials for test users:')
        self.stdout.write('  Password: Test@1234')
        self.stdout.write('')
        self.stdout.write('Freelancers:')
        for f in freelancers:
            self.stdout.write(f"  {f['email']}")
        self.stdout.write('')
        self.stdout.write('Companies:')
        for c in companies:
            self.stdout.write(f"  {c['email']}")