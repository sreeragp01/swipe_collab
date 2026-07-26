from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from profiles.models import CompanyProfile, FreelancerProfile, Skill
from projects.models import Project

User = get_user_model()


class SwipeFeedTestCase(APITestCase):
    def setUp(self):
        self.freelancer_user = User.objects.create_user(
            username="freelancer_swipe",
            email="freelancer_swipe@example.com",
            password="Password123!",
            role="freelancer",
            is_verified=True,
            face_verified=True,
            is_paid=True,
        )
        self.freelancer_profile = FreelancerProfile.objects.create(
            user=self.freelancer_user,
            name="Alice Freelancer",
        )

        self.company_user = User.objects.create_user(
            username="company_swipe",
            email="company_swipe@example.com",
            password="Password123!",
            role="company",
            is_verified=True,
            face_verified=True,
            is_paid=True,
        )
        self.company_profile = CompanyProfile.objects.create(
            user=self.company_user,
            name="TechCorp",
            description="Innovative Tech Solutions",
        )
        self.project = Project.objects.create(
            company=self.company_profile,
            title="Fullstack Web App",
            description="Build a React & Django platform",
            budget_min="15000.00",
            budget_max="30000.00",
            duration="1_3_months",
            status="open",
        )
        self.skill = Skill.objects.create(name="React")
        self.project.skills.add(self.skill)

    def test_freelancer_swipe_feed_contains_open_projects(self):
        self.client.force_authenticate(user=self.freelancer_user)
        response = self.client.get("/api/v1/swipe/feed/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn("feed", data)
        self.assertGreater(len(data["feed"]), 0)
        card = data["feed"][0]
        self.assertIn("open_projects", card)
        self.assertEqual(len(card["open_projects"]), 1)
        self.assertEqual(card["open_projects"][0]["title"], "Fullstack Web App")
        self.assertEqual(float(card["open_projects"][0]["budget_min"]), 15000.0)
