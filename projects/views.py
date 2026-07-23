from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from profiles.models import CompanyProfile, FreelancerProfile
from .models import Project, Application
from .serializers import ProjectSerializer, ApplicationSerializer, CreateApplicationSerializer


class ProjectListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        queryset = Project.objects.filter(status=Project.STATUS_OPEN)
        skill = self.request.query_params.get('skill')
        duration = self.request.query_params.get('duration')
        budget_min = self.request.query_params.get('budget_min')
        if skill:
            queryset = queryset.filter(skills__name__icontains=skill)
        if duration:
            queryset = queryset.filter(duration=duration)
        if budget_min:
            queryset = queryset.filter(budget_max__gte=budget_min)
        return queryset.distinct()


class ProjectCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_company:
            return Response({'detail': 'Only companies can post projects.'}, status=status.HTTP_403_FORBIDDEN)
        try:
            company = request.user.company_profile
        except CompanyProfile.DoesNotExist:
            return Response({'detail': 'Create a company profile first.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            project = serializer.save(company=company)
            try:
                stats = request.user.engagement_stats
                stats.increment('projects_posted')
            except Exception:
                pass
            return Response(ProjectSerializer(project).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
            return Response(ProjectSerializer(project).data)
        except Project.DoesNotExist:
            return Response({'detail': 'Project not found.'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        try:
            project = Project.objects.get(pk=pk, company__user=request.user)
        except Project.DoesNotExist:
            return Response({'detail': 'Not found or not your project.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            project = Project.objects.get(pk=pk, company__user=request.user)
            project.delete()
            return Response({'message': 'Project deleted.'}, status=status.HTTP_204_NO_CONTENT)
        except Project.DoesNotExist:
            return Response({'detail': 'Not found or not your project.'}, status=status.HTTP_404_NOT_FOUND)


class MyProjectsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_company:
            return Response({'detail': 'Only companies have projects.'}, status=status.HTTP_403_FORBIDDEN)
        try:
            projects = Project.objects.filter(company__user=request.user)
            return Response(ProjectSerializer(projects, many=True).data)
        except Exception:
            return Response([])


class ApplicationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        try:
            project = Project.objects.get(pk=project_id, company__user=request.user)
        except Project.DoesNotExist:
            return Response({'detail': 'Not found or not your project.'}, status=status.HTTP_404_NOT_FOUND)
        applications = Application.objects.filter(project=project).select_related('freelancer')
        return Response(ApplicationSerializer(applications, many=True).data)

    def post(self, request, project_id):
        if not request.user.is_freelancer:
            return Response({'detail': 'Only freelancers can apply.'}, status=status.HTTP_403_FORBIDDEN)
        if not request.user.has_access:
            return Response({'detail': 'Active trial or paid plan required.'}, status=status.HTTP_403_FORBIDDEN)
        try:
            project = Project.objects.get(pk=project_id, status=Project.STATUS_OPEN)
        except Project.DoesNotExist:
            return Response({'detail': 'Project not found or not open.'}, status=status.HTTP_404_NOT_FOUND)
        try:
            freelancer = request.user.freelancer_profile
        except FreelancerProfile.DoesNotExist:
            return Response({'detail': 'Create a freelancer profile first.'}, status=status.HTTP_400_BAD_REQUEST)

        if Application.objects.filter(project=project, freelancer=freelancer).exists():
            return Response({'detail': 'You have already applied to this project.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CreateApplicationSerializer(data=request.data)
        if serializer.is_valid():
            application = serializer.save(project=project, freelancer=freelancer)
            try:
                stats = request.user.engagement_stats
                stats.increment('applications_sent')
                company_stats = project.company.user.engagement_stats
                company_stats.increment('applications_received')
            except Exception:
                pass
            return Response(ApplicationSerializer(application).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApplicationStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, project_id, application_id):
        try:
            project = Project.objects.get(pk=project_id, company__user=request.user)
            application = Application.objects.get(pk=application_id, project=project)
        except (Project.DoesNotExist, Application.DoesNotExist):
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get('status')
        valid = [s[0] for s in Application.STATUS_CHOICES]
        if new_status not in valid:
            return Response({'detail': f'Invalid status. Choose from {valid}.'}, status=status.HTTP_400_BAD_REQUEST)

        application.status = new_status
        application.save(update_fields=['status'])
        return Response(ApplicationSerializer(application).data)


class MyApplicationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_freelancer:
            return Response({'detail': 'Only freelancers have applications.'}, status=status.HTTP_403_FORBIDDEN)
        try:
            applications = Application.objects.filter(freelancer__user=request.user)
            return Response(ApplicationSerializer(applications, many=True).data)
        except Exception:
            return Response([])