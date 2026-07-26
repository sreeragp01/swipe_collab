from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from profiles.models import CompanyProfile, FreelancerProfile, Skill
from projects.models import Project, Application

User = get_user_model()


class ProjectAPITestCase(APITestCase):
    def setUp(self):
        self.company_user = User.objects.create_user(
            username="company_user",
            email="company@example.com",
            password="Password123!",
            role="company",
            is_verified=True,
            face_verified=True,
            is_paid=True,
        )
        self.company_profile = CompanyProfile.objects.create(
            user=self.company_user,
            name="Acme Corp",
            description="Leading Tech Corp",
        )
        self.freelancer_user = User.objects.create_user(
            username="freelancer_user",
            email="freelancer@example.com",
            password="Password123!",
            role="freelancer",
            is_verified=True,
            face_verified=True,
            is_paid=True,
        )
        self.freelancer_profile = FreelancerProfile.objects.create(
            user=self.freelancer_user,
            name="John Freelancer",
        )

    def test_create_project_without_skills(self):
        self.client.force_authenticate(user=self.company_user)
        data = {
            "title": "Build API",
            "description": "Django REST API project",
            "budget_min": "5000.00",
            "budget_max": "10000.00",
            "duration": "1_3_months",
        }
        response = self.client.post("/api/v1/projects/create/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 1)
        project = Project.objects.first()
        self.assertEqual(project.title, "Build API")
        self.assertEqual(project.company, self.company_profile)

    def test_create_project_with_skill_names(self):
        self.client.force_authenticate(user=self.company_user)
        data = {
            "title": "Mobile App Development",
            "description": "Flutter app development",
            "budget_min": "10000.00",
            "budget_max": "20000.00",
            "duration": "3_6_months",
            "skill_names": ["Flutter", "Dart", "Firebase"],
        }
        response = self.client.post("/api/v1/projects/create/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        project = Project.objects.get(title="Mobile App Development")
        skill_names = list(project.skills.values_list("name", flat=True))
        self.assertIn("Flutter", skill_names)
        self.assertIn("Dart", skill_names)
        self.assertIn("Firebase", skill_names)
