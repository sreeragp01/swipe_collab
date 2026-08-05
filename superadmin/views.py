from django.contrib.auth import get_user_model
from django.db.models import Q, Sum, Count
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserSerializer
from projects.models import Project, Application
from moderation.models import Report, UserStrike, BlockList
from payments.models import Payment
from swipe.models import SwipeAction
from matches.models import Match
from chat.models import Message

User = get_user_model()


class SuperAdminOverviewView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_users = User.objects.count()
        freelancers = User.objects.filter(role=User.ROLE_FREELANCER).count()
        companies = User.objects.filter(role=User.ROLE_COMPANY).count()
        verified = User.objects.filter(is_verified=True).count()
        face_verified = User.objects.filter(face_verified=True).count()
        paid_users = User.objects.filter(is_paid=True).count()
        trial_users = User.objects.filter(is_trial_active=True).count()
        banned_users = User.objects.filter(is_active=False).count()

        total_projects = Project.objects.count()
        open_projects = Project.objects.filter(status=Project.STATUS_OPEN).count()
        in_progress_projects = Project.objects.filter(status=Project.STATUS_IN_PROGRESS).count()
        completed_projects = Project.objects.filter(status=Project.STATUS_COMPLETED).count()
        total_applications = Application.objects.count()

        total_swipes = SwipeAction.objects.count()
        total_matches = Match.objects.count()
        total_messages = Message.objects.count()

        pending_reports = Report.objects.filter(status=Report.STATUS_PENDING).count()
        total_reports = Report.objects.count()

        successful_payments = Payment.objects.filter(status=Payment.STATUS_SUCCESS)
        total_revenue_paisa = successful_payments.aggregate(total=Sum('amount_paisa'))['total'] or 0
        total_revenue_inr = round(total_revenue_paisa / 100, 2)

        return Response({
            'users': {
                'total': total_users,
                'freelancers': freelancers,
                'companies': companies,
                'verified': verified,
                'face_verified': face_verified,
                'paid': paid_users,
                'trial': trial_users,
                'banned': banned_users,
            },
            'projects': {
                'total': total_projects,
                'open': open_projects,
                'in_progress': in_progress_projects,
                'completed': completed_projects,
                'applications': total_applications,
            },
            'engagement': {
                'swipes': total_swipes,
                'matches': total_matches,
                'messages': total_messages,
            },
            'moderation': {
                'pending_reports': pending_reports,
                'total_reports': total_reports,
            },
            'payments': {
                'total_transactions': Payment.objects.count(),
                'successful_transactions': successful_payments.count(),
                'total_revenue_inr': total_revenue_inr,
            }
        })


class SuperAdminUserListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        qs = User.objects.all().order_by('-date_joined')

        search = request.query_params.get('search', '').strip()
        if search:
            qs = qs.filter(
                Q(email__icontains=search) |
                Q(username__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )

        role = request.query_params.get('role', '').strip()
        if role in [User.ROLE_FREELANCER, User.ROLE_COMPANY]:
            qs = qs.filter(role=role)

        is_verified = request.query_params.get('is_verified')
        if is_verified is not None and is_verified != '':
            qs = qs.filter(is_verified=is_verified.lower() == 'true')

        is_paid = request.query_params.get('is_paid')
        if is_paid is not None and is_paid != '':
            qs = qs.filter(is_paid=is_paid.lower() == 'true')

        is_active = request.query_params.get('is_active')
        if is_active is not None and is_active != '':
            qs = qs.filter(is_active=is_active.lower() == 'true')

        users_data = []
        for user in qs[:100]:
            data = UserSerializer(user, context={'request': request}).data
            data['strikes'] = getattr(getattr(user, 'userstrike', None), 'strike_count', 0)
            data['reports_against_count'] = Report.objects.filter(reported_user=user).count()
            users_data.append(data)

        return Response({
            'count': qs.count(),
            'users': users_data
        })


class SuperAdminUserDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        data = UserSerializer(user, context={'request': request}).data
        strike_obj = getattr(user, 'userstrike', None)
        data['strikes'] = strike_obj.strike_count if strike_obj else 0
        data['is_banned'] = not user.is_active
        data['reports_against'] = [
            {
                'id': r.id,
                'reporter_email': r.reporter.email if r.reporter else 'Anonymous',
                'category': r.category,
                'reason': r.reason,
                'status': r.status,
                'created_at': r.created_at,
            }
            for r in Report.objects.filter(reported_user=user).order_by('-created_at')
        ]
        return Response(data)

    def patch(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        updatable_fields = [
            'is_verified', 'face_verified', 'is_paid', 'is_trial_active',
            'is_active', 'is_staff', 'is_superuser', 'role'
        ]

        fields_to_update = []
        for field in updatable_fields:
            if field in data:
                setattr(user, field, data[field])
                fields_to_update.append(field)

        if fields_to_update:
            user.save(update_fields=fields_to_update)

        action = data.get('action')
        if action == 'start_trial':
            user.start_trial()
        elif action == 'issue_strike':
            strike, _ = UserStrike.objects.get_or_create(user=user)
            strike.add_strike()
        elif action == 'reset_strikes':
            UserStrike.objects.filter(user=user).update(strike_count=0)

        updated_data = UserSerializer(user, context={'request': request}).data
        strike_obj = getattr(user, 'userstrike', None)
        updated_data['strikes'] = strike_obj.strike_count if strike_obj else 0
        return Response({
            'message': f'User {user.email} updated successfully.',
            'user': updated_data
        })


class SuperAdminProjectListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        qs = Project.objects.select_related('company', 'company__user').all().order_by('-created_at')

        search = request.query_params.get('search', '').strip()
        if search:
            qs = qs.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(company__user__email__icontains=search) |
                Q(company__company_name__icontains=search)
            )

        status_filter = request.query_params.get('status', '').strip()
        if status_filter:
            qs = qs.filter(status=status_filter)

        projects_data = []
        for p in qs[:100]:
            projects_data.append({
                'id': str(p.id),
                'title': p.title,
                'category': p.category,
                'status': p.status,
                'budget': str(p.budget),
                'company_email': p.company.user.email if p.company and p.company.user else 'Unknown',
                'company_name': p.company.company_name if p.company else 'Company',
                'applications_count': p.applications.count(),
                'created_at': p.created_at,
            })

        return Response({
            'count': qs.count(),
            'projects': projects_data
        })


class SuperAdminProjectDetailView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response({'detail': 'Project not found.'}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get('status')
        if new_status:
            project.status = new_status
            project.save(update_fields=['status'])
            return Response({'message': f'Project status updated to {new_status}.'})

        return Response({'detail': 'No changes provided.'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
            title = project.title
            project.delete()
            return Response({'message': f'Project "{title}" deleted successfully.'}, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({'detail': 'Project not found.'}, status=status.HTTP_404_NOT_FOUND)


class SuperAdminReportListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        qs = Report.objects.select_related('reporter', 'reported_user', 'reviewed_by').all().order_by('-created_at')

        status_filter = request.query_params.get('status', '').strip()
        if status_filter:
            qs = qs.filter(status=status_filter)

        category = request.query_params.get('category', '').strip()
        if category:
            qs = qs.filter(category=category)

        reports_data = []
        for r in qs[:100]:
            reports_data.append({
                'id': r.id,
                'reporter_email': r.reporter.email if r.reporter else 'Anonymous',
                'reported_user_id': str(r.reported_user.id) if r.reported_user else None,
                'reported_user_email': r.reported_user.email if r.reported_user else 'Unknown',
                'reported_user_banned': not r.reported_user.is_active if r.reported_user else False,
                'category': r.category,
                'reason': r.reason,
                'evidence_url': r.evidence_url,
                'status': r.status,
                'reviewed_by_email': r.reviewed_by.email if r.reviewed_by else None,
                'created_at': r.created_at,
            })

        return Response({
            'count': qs.count(),
            'reports': reports_data
        })


class SuperAdminReportActionView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        try:
            report = Report.objects.get(pk=pk)
        except Report.DoesNotExist:
            return Response({'detail': 'Report not found.'}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get('status')
        issue_strike = request.data.get('issue_strike', False)
        ban_user = request.data.get('ban_user', False)

        if new_status:
            report.status = new_status
            report.reviewed_by = request.user
            report.save(update_fields=['status', 'reviewed_by'])

        if issue_strike and report.reported_user:
            strike, _ = UserStrike.objects.get_or_create(user=report.reported_user)
            strike.add_strike()

        if ban_user and report.reported_user:
            report.reported_user.is_active = False
            report.reported_user.save(update_fields=['is_active'])

        return Response({
            'message': f'Report #{report.id} updated.',
            'status': report.status,
            'reported_user_active': report.reported_user.is_active if report.reported_user else True,
        })


class SuperAdminPaymentListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        qs = Payment.objects.select_related('user').all().order_by('-created_at')

        status_filter = request.query_params.get('status', '').strip()
        if status_filter:
            qs = qs.filter(status=status_filter)

        search = request.query_params.get('search', '').strip()
        if search:
            qs = qs.filter(
                Q(user__email__icontains=search) |
                Q(rzp_order_id__icontains=search) |
                Q(rzp_payment_id__icontains=search)
            )

        payments_data = []
        for p in qs[:100]:
            payments_data.append({
                'id': str(p.id),
                'user_email': p.user.email if p.user else 'Unknown',
                'rzp_order_id': p.rzp_order_id,
                'rzp_payment_id': p.rzp_payment_id or '—',
                'amount_inr': p.amount_inr,
                'status': p.status,
                'created_at': p.created_at,
            })

        return Response({
            'count': qs.count(),
            'payments': payments_data
        })
