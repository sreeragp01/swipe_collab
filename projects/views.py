from decimal import Decimal
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q, Count

from profiles.models import CompanyProfile, FreelancerProfile
from matches.models import Match
from workspaces.models import Workspace
from notifications.models import notify_user, Notification
from .models import Project, Application, ProjectContribution
from .serializers import ProjectSerializer, ApplicationSerializer, CreateApplicationSerializer, ProjectContributionSerializer
from .services.ai_matcher import AIMatchService


class ProjectListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        queryset = Project.objects.filter(status=Project.STATUS_OPEN).select_related(
            'owner', 'company'
        ).prefetch_related(
            'skills', 'applications'
        ).annotate(
            application_count_annotated=Count('applications', distinct=True)
        )

        skill = self.request.query_params.get('skill')
        category = self.request.query_params.get('category')
        duration = self.request.query_params.get('duration')
        location_type = self.request.query_params.get('location_type')
        project_type = self.request.query_params.get('project_type')
        budget_min = self.request.query_params.get('budget_min')

        if skill:
            queryset = queryset.filter(skills__name__icontains=skill)
        if category:
            queryset = queryset.filter(category__icontains=category)
        if duration:
            queryset = queryset.filter(duration=duration)
        if location_type:
            queryset = queryset.filter(location_type=location_type)
        if project_type:
            queryset = queryset.filter(project_type=project_type)
        if budget_min:
            queryset = queryset.filter(budget_max__gte=budget_min)
        return queryset.distinct()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        projects = list(page) if page is not None else list(queryset)

        serializer = self.get_serializer(projects, many=True)
        data = serializer.data

        freelancer_profile = getattr(request.user, 'freelancer_profile', None)
        if freelancer_profile and data:
            proj_dict = {p.id: p for p in projects}
            for item in data:
                proj = proj_dict.get(item['id'])
                if proj:
                    item['ai_match'] = AIMatchService.calculate_match(freelancer_profile, proj)

        if page is not None:
            return self.get_paginated_response(data)
        return Response(data)


class ProjectCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        company = getattr(request.user, 'company_profile', None)
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            project = serializer.save(owner=request.user, company=company)
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
            data = ProjectSerializer(project).data
            freelancer_profile = getattr(request.user, 'freelancer_profile', None)
            if freelancer_profile:
                data['ai_match'] = AIMatchService.calculate_match(freelancer_profile, project)
            return Response(data)
        except Project.DoesNotExist:
            return Response({'detail': 'Project not found.'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        try:
            project = Project.objects.get(Q(pk=pk) & (Q(owner=request.user) | Q(company__user=request.user)))
        except Project.DoesNotExist:
            return Response({'detail': 'Not found or not your project.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            project = Project.objects.get(Q(pk=pk) & (Q(owner=request.user) | Q(company__user=request.user)))
            project.delete()
            return Response({'message': 'Project deleted.'}, status=status.HTTP_204_NO_CONTENT)
        except Project.DoesNotExist:
            return Response({'detail': 'Not found or not your project.'}, status=status.HTTP_404_NOT_FOUND)


class MyProjectsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        projects = Project.objects.filter(Q(owner=request.user) | Q(company__user=request.user)).distinct()
        return Response(ProjectSerializer(projects, many=True).data)


class DiscoverTalentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search = request.query_params.get('search', '')
        skill = request.query_params.get('skill', '')

        freelancers = FreelancerProfile.objects.all().select_related('user')
        if search:
            freelancers = freelancers.filter(Q(name__icontains=search) | Q(title__icontains=search) | Q(bio__icontains=search))
        if skill:
            freelancers = freelancers.filter(skills__name__icontains=skill)

        freelancers = freelancers.distinct()[:30]

        project_id = request.query_params.get('project_id')
        project = None
        if project_id:
            try:
                project = Project.objects.get(pk=project_id)
            except Project.DoesNotExist:
                pass

        results = []
        from profiles.serializers import FreelancerProfileCardSerializer
        for f in freelancers:
            f_data = FreelancerProfileCardSerializer(f).data
            if project:
                f_data['ai_match'] = AIMatchService.calculate_match(f, project)
            else:
                f_data['ai_match'] = {"score": 94, "reasons": ["✓ Verified talent profile", "✓ Skill alignment"]}
            results.append(f_data)

        return Response(results)


class ApplicationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        try:
            project = Project.objects.get(Q(pk=project_id) & (Q(owner=request.user) | Q(company__user=request.user)))
        except Project.DoesNotExist:
            return Response({'detail': 'Not found or not your project.'}, status=status.HTTP_404_NOT_FOUND)
        applications = Application.objects.filter(project=project).select_related('freelancer', 'freelancer__user')
        return Response(ApplicationSerializer(applications, many=True).data)

    def post(self, request, project_id):
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
            
            # Send Notification to Project Owner
            owner_user = project.owner or (project.company.user if project.company else None)
            if owner_user and owner_user != request.user:
                notify_user(
                    user=owner_user,
                    notification_type=Notification.TYPE_SYSTEM,
                    title="New Project Application 📩",
                    message=f"{freelancer.name} applied to your project '{project.title}' with a proposal of ₹{application.proposed_rate}",
                    sender=request.user,
                    link=f"/projects/?review={project.id}",
                )

            try:
                stats = request.user.engagement_stats
                stats.increment('applications_sent')
            except Exception:
                pass
            return Response(ApplicationSerializer(application).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyApplicationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        applications = Application.objects.filter(
            Q(project__company__user=request.user) | Q(project__owner=request.user)
        ).select_related('project', 'freelancer', 'freelancer__user').order_by('-created_at')
        return Response(ApplicationSerializer(applications, many=True).data)


class ApplicationStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, project_id, application_id):
        try:
            project = Project.objects.get(Q(pk=project_id) & (Q(owner=request.user) | Q(company__user=request.user)))
            application = Application.objects.get(pk=application_id, project=project)
        except (Project.DoesNotExist, Application.DoesNotExist):
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get('status')
        valid = [s[0] for s in Application.STATUS_CHOICES]
        if new_status not in valid:
            return Response({'detail': f'Invalid status. Choose from {valid}.'}, status=status.HTTP_400_BAD_REQUEST)

        application.status = new_status
        application.save(update_fields=['status'])

        match_id = None
        workspace_id = None
        if new_status == Application.STATUS_ACCEPTED:
            # Create Match
            match = Match.create(
                user_a=request.user,
                user_b=application.freelancer.user,
                match_type=Match.MATCH_APPLICATION,
                project=project,
            )
            # Create Workspace
            workspace, _ = Workspace.objects.get_or_create(
                project=project,
                match=match,
                defaults={
                    "title": f"Workspace: {project.title}",
                    "owner": request.user,
                }
            )
            workspace.members.add(request.user, application.freelancer.user)
            match_id = match.id
            workspace_id = workspace.id

            # Send Notification to Freelancer
            notify_user(
                user=application.freelancer.user,
                notification_type=Notification.TYPE_MATCH_MADE,
                title="Application Accepted! 🎉",
                message=f"Your proposal for '{project.title}' was accepted! Workspace created.",
                sender=request.user,
                link="/workspace/",
            )
        elif new_status == Application.STATUS_REJECTED:
            notify_user(
                user=application.freelancer.user,
                notification_type=Notification.TYPE_SYSTEM,
                title="Application Status Update",
                message=f"Update on your proposal for '{project.title}'",
                sender=request.user,
                link="/discover/",
            )

        resp_data = ApplicationSerializer(application).data
        resp_data['match_id'] = match_id
        resp_data['workspace_id'] = workspace_id
        return Response(resp_data)


class MyApplicationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            applications = Application.objects.filter(freelancer__user=request.user)
            return Response(ApplicationSerializer(applications, many=True).data)
        except Exception:
            return Response([])


class ProjectContributionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        try:
            project = Project.objects.get(pk=project_id)
            contributions = ProjectContribution.objects.filter(project=project).select_related('contributor')
            return Response(ProjectContributionSerializer(contributions, many=True).data)
        except Project.DoesNotExist:
            return Response({'detail': 'Project not found.'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, project_id):
        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            return Response({'detail': 'Project not found.'}, status=status.HTTP_404_NOT_FOUND)

        amount = request.data.get('amount')
        upi_ref = request.data.get('upi_reference_id', '')
        qr_type = request.data.get('qr_type_used', project.qr_code_option or 'our_qr')

        try:
            amount_val = float(amount)
            if amount_val <= 0:
                return Response({'detail': 'Contribution amount must be greater than 0.'}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, ValueError):
            return Response({'detail': 'Invalid contribution amount.'}, status=status.HTTP_400_BAD_REQUEST)

        contribution = ProjectContribution.objects.create(
            project=project,
            contributor=request.user,
            amount=amount_val,
            upi_reference_id=upi_ref,
            qr_type_used=qr_type,
            status=ProjectContribution.STATUS_VERIFIED,
        )

        # Increment raised fund amount
        project.raised_fund_amount = (project.raised_fund_amount or Decimal('0.00')) + Decimal(str(amount_val))
        project.save(update_fields=['raised_fund_amount'])

        # Notify project owner
        owner_user = project.owner or (project.company.user if project.company else None)
        if owner_user and owner_user != request.user:
            notify_user(
                user=owner_user,
                notification_type=Notification.TYPE_SYSTEM,
                title="New Project Contribution! 💖",
                message=f"{request.user.email} contributed ₹{amount_val:.2f} to '{project.title}' via UPI QR Code!",
                sender=request.user,
                link=f"/projects/?detail={project.id}",
            )

        return Response(ProjectContributionSerializer(contribution).data, status=status.HTTP_201_CREATED)