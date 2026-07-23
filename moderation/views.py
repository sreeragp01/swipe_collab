from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Report, BlockList, UserStrike
from .serializers import ReportSerializer, BlockListSerializer, UserStrikeSerializer

User = get_user_model()


class ReportUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        reported_id = request.data.get('reported_user')
        if not reported_id:
            return Response({'detail': 'reported_user is required.'}, status=status.HTTP_400_BAD_REQUEST)
        if str(reported_id) == str(request.user.id):
            return Response({'detail': 'You cannot report yourself.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            reported_user = User.objects.get(id=reported_id)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(reporter=request.user, reported_user=reported_user)
            return Response({'message': 'Report submitted successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        reports = Report.objects.filter(reporter=request.user)
        return Response(ReportSerializer(reports, many=True).data)


class BlockUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        blocked_id = request.data.get('blocked')
        if not blocked_id:
            return Response({'detail': 'blocked user id is required.'}, status=status.HTTP_400_BAD_REQUEST)
        if str(blocked_id) == str(request.user.id):
            return Response({'detail': 'You cannot block yourself.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            blocked_user = User.objects.get(id=blocked_id)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if BlockList.objects.filter(blocker=request.user, blocked=blocked_user).exists():
            return Response({'detail': 'User is already blocked.'}, status=status.HTTP_400_BAD_REQUEST)

        block = BlockList.objects.create(
            blocker=request.user,
            blocked=blocked_user,
            reason=request.data.get('reason', ''),
        )
        return Response(BlockListSerializer(block).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        blocked = BlockList.objects.filter(blocker=request.user)
        return Response(BlockListSerializer(blocked, many=True).data)


class UnblockUserView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, blocked_id):
        try:
            block = BlockList.objects.get(blocker=request.user, blocked__id=blocked_id)
            block.delete()
            return Response({'message': 'User unblocked.'}, status=status.HTTP_204_NO_CONTENT)
        except BlockList.DoesNotExist:
            return Response({'detail': 'Block not found.'}, status=status.HTTP_404_NOT_FOUND)


class AdminReportListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        reports = Report.objects.filter(status=Report.STATUS_PENDING)
        return Response(ReportSerializer(reports, many=True).data)


class AdminReportActionView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, report_id):
        try:
            report = Report.objects.get(pk=report_id)
        except Report.DoesNotExist:
            return Response({'detail': 'Report not found.'}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get('status')
        issue_strike = request.data.get('issue_strike', False)

        if new_status:
            report.status = new_status
            report.reviewed_by = request.user
            report.save(update_fields=['status', 'reviewed_by'])

        if issue_strike and new_status == Report.STATUS_ACTIONED:
            strike, _ = UserStrike.objects.get_or_create(user=report.reported_user)
            strike.add_strike()

        return Response(ReportSerializer(report).data)