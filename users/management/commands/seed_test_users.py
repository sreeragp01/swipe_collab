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
                'title': 'Senior Full Stack Django & React Developer',
                'bio': 'Versatile Full Stack Engineer with 4+ years of hands-on experience building enterprise SaaS applications, REST APIs, and dynamic real-time web applications with Django and React.',
                'avatar_data': 'https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?auto=format&fit=crop&w=400&q=80',
                'experience_years': 4,
                'hourly_rate': 55.00,
                'hours_per_week': 'more_than_30',
                'english_fluency': 'fluent',
                'availability': 'full_time',
                'city': 'Bangalore',
                'country': 'India',
                'skills': ['Python', 'Django', 'React', 'PostgreSQL'],
                'portfolio_url': 'https://alexjohnson.dev',
                'github_url': 'https://github.com/alex-dev',
                'linkedin_url': 'https://linkedin.com/in/alex-johnson-dev',
                'video_intro_url': 'https://www.w3schools.com/html/mov_bbb.mp4',
                'education': [
                    {
                        'school': 'Indian Institute of Technology (IIT) Bombay',
                        'degree': 'B.Tech in Computer Science & Engineering',
                        'year': '2016 - 2020'
                    }
                ],
                'certifications': [
                    {
                        'name': 'AWS Certified Developer – Associate',
                        'issuer': 'Amazon Web Services',
                        'year': '2022'
                    }
                ],
            },
            {
                'email': 'priya@test.com',
                'username': 'priya_ui',
                'name': 'Priya Sharma',
                'title': 'Lead UI/UX Designer & Design Systems Specialist',
                'bio': 'Passionate Product Designer with 3+ years experience transforming complex user journeys into sleek, high-converting mobile apps and web interfaces with Figma and Tailwind.',
                'avatar_data': 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=400&q=80',
                'experience_years': 3,
                'hourly_rate': 50.00,
                'hours_per_week': 'more_than_30',
                'english_fluency': 'native_bilingual',
                'availability': 'part_time',
                'city': 'Mumbai',
                'country': 'India',
                'skills': ['UI/UX Design', 'Figma', 'Adobe XD', 'Prototyping'],
                'portfolio_url': 'https://priyasharma.design',
                'github_url': 'https://github.com/priya-ui',
                'linkedin_url': 'https://linkedin.com/in/priya-sharma-ux',
                'video_intro_url': 'https://www.w3schools.com/html/mov_bbb.mp4',
                'education': [
                    {
                        'school': 'National Institute of Design (NID)',
                        'degree': 'Bachelor of Design (B.Des) in Interaction Design',
                        'year': '2017 - 2021'
                    }
                ],
                'certifications': [
                    {
                        'name': 'Google UX Design Professional Certificate',
                        'issuer': 'Coursera / Google',
                        'year': '2022'
                    }
                ],
            },
            {
                'email': 'rahul@test.com',
                'username': 'rahul_ml',
                'name': 'Rahul Nair',
                'title': 'Senior Machine Learning & NLP Engineer',
                'bio': 'AI/ML specialist with 5 years experience designing Deep Learning pipelines, Large Language Model fine-tuning, Transformers, and Computer Vision solutions for healthcare & fintech.',
                'avatar_data': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=400&q=80',
                'experience_years': 5,
                'hourly_rate': 75.00,
                'hours_per_week': 'more_than_30',
                'english_fluency': 'fluent',
                'availability': 'contract',
                'city': 'Hyderabad',
                'country': 'India',
                'skills': ['Python', 'Machine Learning', 'TensorFlow', 'NLP'],
                'portfolio_url': 'https://rahulnair.ai',
                'github_url': 'https://github.com/rahul-ml',
                'linkedin_url': 'https://linkedin.com/in/rahul-nair-ml',
                'video_intro_url': 'https://www.w3schools.com/html/mov_bbb.mp4',
                'education': [
                    {
                        'school': 'IIT Hyderabad',
                        'degree': 'M.Tech in Artificial Intelligence',
                        'year': '2017 - 2019'
                    }
                ],
                'certifications': [
                    {
                        'name': 'TensorFlow Developer Certificate',
                        'issuer': 'Google',
                        'year': '2021'
                    }
                ],
            },
            {
                'email': 'sara@test.com',
                'username': 'sara_mobile',
                'name': 'Sara Thomas',
                'title': 'Cross-Platform Mobile App Lead (Flutter & React Native)',
                'bio': 'Mobile App Developer building high-performance cross-platform iOS & Android applications with Flutter, Firebase, clean state management, and smooth 60fps UI animations.',
                'avatar_data': 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=400&q=80',
                'experience_years': 3,
                'hourly_rate': 45.00,
                'hours_per_week': 'more_than_30',
                'english_fluency': 'fluent',
                'availability': 'full_time',
                'city': 'Kochi',
                'country': 'India',
                'skills': ['Flutter', 'React Native', 'Kotlin', 'Firebase'],
                'portfolio_url': 'https://sarathomas.dev',
                'github_url': 'https://github.com/sara-mobile',
                'linkedin_url': 'https://linkedin.com/in/sara-thomas-mobile',
                'video_intro_url': 'https://www.w3schools.com/html/mov_bbb.mp4',
                'education': [
                    {
                        'school': 'Cochin University of Science and Technology',
                        'degree': 'B.Tech in Computer Science',
                        'year': '2018 - 2022'
                    }
                ],
                'certifications': [
                    {
                        'name': 'Associate Android Developer',
                        'issuer': 'Google',
                        'year': '2023'
                    }
                ],
            },
            {
                'email': 'arjun@test.com',
                'username': 'arjun_devops',
                'name': 'Arjun Menon',
                'title': 'DevOps & Cloud Infrastructure Architect (CKA)',
                'bio': 'DevOps Engineer specializing in enterprise cloud infrastructure, Kubernetes clusters, Docker container orchestration, and automated GitOps CI/CD pipelines.',
                'avatar_data': 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=400&q=80',
                'experience_years': 6,
                'hourly_rate': 80.00,
                'hours_per_week': 'more_than_30',
                'english_fluency': 'native_bilingual',
                'availability': 'full_time',
                'city': 'Pune',
                'country': 'India',
                'skills': ['Docker', 'Kubernetes', 'AWS', 'CI/CD'],
                'portfolio_url': 'https://arjunmenon.dev',
                'github_url': 'https://github.com/arjun-devops',
                'linkedin_url': 'https://linkedin.com/in/arjun-menon-dev',
                'video_intro_url': 'https://www.w3schools.com/html/mov_bbb.mp4',
                'education': [
                    {
                        'school': 'BITS Pilani',
                        'degree': 'B.E. in Computer Science',
                        'year': '2014 - 2018'
                    }
                ],
                'certifications': [
                    {
                        'name': 'Certified Kubernetes Administrator (CKA)',
                        'issuer': 'Cloud Native Computing Foundation',
                        'year': '2023'
                    },
                    {
                        'name': 'AWS Certified Solutions Architect – Professional',
                        'issuer': 'Amazon Web Services',
                        'year': '2024'
                    }
                ],
            },
            {
                'email': 'neha@test.com',
                'username': 'neha_frontend',
                'name': 'Neha Gupta',
                'title': 'Senior Frontend Architect | Next.js & React Specialist',
                'bio': 'Senior Frontend Developer specializing in React, Next.js, TypeScript, and high-performance Web UI architecture with responsive design systems.',
                'avatar_data': 'https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&w=400&q=80',
                'experience_years': 5,
                'hourly_rate': 65.00,
                'hours_per_week': 'more_than_30',
                'english_fluency': 'native_bilingual',
                'availability': 'full_time',
                'city': 'Delhi',
                'country': 'India',
                'skills': ['React', 'Next.js', 'TypeScript', 'TailwindCSS'],
                'portfolio_url': 'https://nehagupta.design',
                'github_url': 'https://github.com/neha-frontend',
                'linkedin_url': 'https://linkedin.com/in/neha-gupta-ui',
                'video_intro_url': 'https://www.w3schools.com/html/mov_bbb.mp4',
                'education': [
                    {
                        'school': 'Delhi Technological University (DTU)',
                        'degree': 'B.Tech in Information Technology',
                        'year': '2015 - 2019'
                    }
                ],
                'certifications': [
                    {
                        'name': 'Meta Front-End Developer Professional Certificate',
                        'issuer': 'Meta',
                        'year': '2022'
                    }
                ],
            },
            {
                'email': 'vikram@test.com',
                'username': 'vikram_cyber',
                'name': 'Vikram Singh',
                'title': 'Cybersecurity Lead & Certified Ethical Hacker (OSCP)',
                'bio': 'Ethical hacker and cybersecurity consultant conducting penetration testing, OWASP vulnerability assessments, and secure cloud API architecture audits.',
                'avatar_data': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=400&q=80',
                'experience_years': 7,
                'hourly_rate': 90.00,
                'hours_per_week': 'less_than_30',
                'english_fluency': 'fluent',
                'availability': 'contract',
                'city': 'Chennai',
                'country': 'India',
                'skills': ['Cybersecurity', 'Penetration Testing', 'Python', 'Docker'],
                'portfolio_url': 'https://vikramsec.io',
                'github_url': 'https://github.com/vikram-cyber',
                'linkedin_url': 'https://linkedin.com/in/vikram-singh-sec',
                'video_intro_url': 'https://www.w3schools.com/html/mov_bbb.mp4',
                'education': [
                    {
                        'school': 'IIT Madras',
                        'degree': 'B.Tech in Computer Science',
                        'year': '2013 - 2017'
                    }
                ],
                'certifications': [
                    {
                        'name': 'Offensive Security Certified Professional (OSCP)',
                        'issuer': 'OffSec',
                        'year': '2021'
                    },
                    {
                        'name': 'Certified Information Systems Security Professional (CISSP)',
                        'issuer': '(ISC)²',
                        'year': '2023'
                    }
                ],
            },
        ]

        # ── Companies ─────────────────────────────────
        companies = [
            {
                'email': 'techcorp@test.com',
                'username': 'techcorp',
                'name': 'TechCorp India',
                'description': 'Leading SaaS innovation hub in India building high-scale multi-tenant enterprise tools, cloud APIs, and web platforms for global markets.',
                'logo_data': 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=400&q=80',
                'website_url': 'https://techcorp.io',
                'city': 'Bangalore',
                'country': 'India',
                'skills': ['Python', 'Django', 'React', 'PostgreSQL'],
            },
            {
                'email': 'designstudio@test.com',
                'username': 'designstudio',
                'name': 'DesignStudio Creative Agency',
                'description': 'Award-winning creative product design studio specializing in mobile UI/UX, interaction design, brand identities, and modern design systems.',
                'logo_data': 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=400&q=80',
                'website_url': 'https://designstudio.agency',
                'city': 'Mumbai',
                'country': 'India',
                'skills': ['UI/UX Design', 'Figma', 'Prototyping'],
            },
            {
                'email': 'ailab@test.com',
                'username': 'ailab',
                'name': 'AI Research Lab',
                'description': 'Deep-tech AI research lab building intelligent Machine Learning models, natural language processing applications, and healthcare diagnostic tools.',
                'logo_data': 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=400&q=80',
                'website_url': 'https://ailab.ai',
                'city': 'Hyderabad',
                'country': 'India',
                'skills': ['Machine Learning', 'Python', 'TensorFlow', 'NLP'],
            },
            {
                'email': 'cybernet@test.com',
                'username': 'cybernet',
                'name': 'CyberShield Solutions',
                'description': 'Premier enterprise cybersecurity consultancy conducting deep vulnerability assessments, threat intelligence, and cloud API penetration testing.',
                'logo_data': 'https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&w=400&q=80',
                'website_url': 'https://cybershield.sec',
                'city': 'Chennai',
                'country': 'India',
                'skills': ['Cybersecurity', 'Penetration Testing', 'Docker', 'Python'],
            },
            {
                'email': 'cloudscale@test.com',
                'username': 'cloudscale',
                'name': 'CloudScale Systems',
                'description': 'High-performance cloud infrastructure engineering firm specializing in AWS cloud migrations, Kubernetes clusters, and microservices.',
                'logo_data': 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=400&q=80',
                'website_url': 'https://cloudscale.labs',
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

        # Create/Update freelancers
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
            user.is_verified = True
            user.face_verified = True
            user.is_paid = True
            user.save()

            profile, _ = FreelancerProfile.objects.get_or_create(user=user)
            profile.name = data['name']
            profile.title = data.get('title', '')
            profile.bio = data['bio']
            profile.avatar_data = data.get('avatar_data', '')
            profile.experience_years = data['experience_years']
            profile.hourly_rate = data.get('hourly_rate', 50.00)
            profile.hours_per_week = data.get('hours_per_week', 'more_than_30')
            profile.english_fluency = data.get('english_fluency', 'fluent')
            profile.availability = data['availability']
            profile.city = data['city']
            profile.country = data['country']
            profile.portfolio_url = data.get('portfolio_url', '')
            profile.github_url = data.get('github_url', '')
            profile.linkedin_url = data.get('linkedin_url', '')
            profile.video_intro_url = data.get('video_intro_url', '')
            profile.education = data.get('education', [])
            profile.certifications = data.get('certifications', [])
            profile.save()

            skills = []
            for s_name in data['skills']:
                sk, _ = Skill.objects.get_or_create(name=s_name, defaults={'category': 'General'})
                skills.append(sk)
            profile.skills.set(skills)

            self.stdout.write(self.style.SUCCESS(f"  [OK] Freelancer Profile Completed: {data['email']}"))
            created_count += 1

        # Create/Update companies
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
            user.is_verified = True
            user.face_verified = True
            user.is_paid = True
            user.save()

            profile, _ = CompanyProfile.objects.get_or_create(user=user)
            profile.name = data['name']
            profile.description = data['description']
            profile.logo_data = data.get('logo_data', '')
            profile.website_url = data.get('website_url', '')
            profile.city = data['city']
            profile.country = data['country']
            profile.save()
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