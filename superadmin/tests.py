from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from projects.models import Project
from moderation.models import Report
from payments.models import Payment

User = get_user_model()


class SuperAdminAPITests(APITestCase):

    def setUp(self):
        # Create normal user
        self.user = User.objects.create_user(
            email='normal@example.com',
            username='normaluser',
            password='password123',
            role=User.ROLE_FREELANCER,
        )

        # Create admin user
        self.admin = User.objects.create_user(
            email='admin@example.com',
            username='adminuser',
            password='password123',
            role=User.ROLE_COMPANY,
            is_staff=True,
            is_superuser=True,
        )

        from profiles.models import CompanyProfile
        self.company_profile = CompanyProfile.objects.create(
            user=self.admin,
            name="Test Company",
        )
        self.project = Project.objects.create(
            company=self.company_profile,
            title="Sample Project",
            description="Sample project description",
            budget_min=100,
            budget_max=500,
            status=Project.STATUS_OPEN,
        )

    def test_unauthorized_access(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/v1/superadmin/overview/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get('/api/v1/superadmin/users/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_overview_api(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('/api/v1/superadmin/overview/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('users', response.data)
        self.assertIn('projects', response.data)
        self.assertIn('moderation', response.data)
        self.assertIn('payments', response.data)
        self.assertEqual(response.data['users']['total'], 2)

    def test_user_management_api(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('/api/v1/superadmin/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

        # Update user attributes
        patch_res = self.client.patch(f'/api/v1/superadmin/users/{self.user.id}/', {
            'is_verified': True,
            'is_paid': True,
        }, format='json')
        self.assertEqual(patch_res.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_verified)
        self.assertTrue(self.user.is_paid)

    def test_ban_unban_user(self):
        self.client.force_authenticate(user=self.admin)
        patch_res = self.client.patch(f'/api/v1/superadmin/users/{self.user.id}/', {
            'is_active': False,
        }, format='json')
        self.assertEqual(patch_res.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_project_list_api(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('/api/v1/superadmin/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        project_data = response.data['projects'][0]
        self.assertEqual(project_data['title'], "Sample Project")
        self.assertEqual(project_data['company_name'], "Test Company")
        self.assertEqual(project_data['budget'], "100.00 - 500.00")

    def test_update_project_status(self):
        self.client.force_authenticate(user=self.admin)
        patch_res = self.client.patch(f'/api/v1/superadmin/projects/{self.project.id}/', {
            'status': 'in_progress',
        }, format='json')
        self.assertEqual(patch_res.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.status, 'in_progress')
