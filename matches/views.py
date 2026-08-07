from django.db.models import Q, Avg
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Match, CollaborationSession, CollaborationRating
from .serializers import (
    MatchSerializer,
    CollaborationSessionSerializer,
    CreateCollaborationSessionSerializer,
)


class MatchListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from chat.models import ChatRoom
        matches = Match.objects.filter(
            Q(user1=request.user) | Q(user2=request.user)
        ).select_related('user1', 'user2')
        for m in matches:
            ChatRoom.objects.get_or_create(match=m)

        serializer = MatchSerializer(
            matches, many=True, context={'request': request}
        )
        return Response({
            'matches': serializer.data,
            'count':   matches.count(),
        })


class MatchDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            match = Match.objects.get(
                Q(pk=pk) & (Q(user1=request.user) | Q(user2=request.user))
            )
            serializer = MatchSerializer(match, context={'request': request})
            return Response(serializer.data)
        except Match.DoesNotExist:
            return Response(
                {'detail': 'Match not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

    def delete(self, request, pk):
        try:
            match = Match.objects.get(
                Q(pk=pk) & (Q(user1=request.user) | Q(user2=request.user))
            )
            match.delete()
            return Response(
                {'message': 'Match removed.'},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Match.DoesNotExist:
            return Response(
                {'detail': 'Match not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )


class CollaborationSessionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, match_id):
        try:
            match = Match.objects.get(
                Q(pk=match_id) & (Q(user1=request.user) | Q(user2=request.user))
            )
        except Match.DoesNotExist:
            return Response(
                {'detail': 'Match not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        sessions   = CollaborationSession.objects.filter(match=match)
        serializer = CollaborationSessionSerializer(sessions, many=True)
        return Response({'sessions': serializer.data})

    def post(self, request, match_id):
        try:
            match = Match.objects.get(
                Q(pk=match_id) & (Q(user1=request.user) | Q(user2=request.user))
            )
        except Match.DoesNotExist:
            return Response(
                {'detail': 'Match not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = CreateCollaborationSessionSerializer(data=request.data)
        if serializer.is_valid():
            session = serializer.save(match=match, initiated_by=request.user)
            return Response(
                CollaborationSessionSerializer(session).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CollaborationSessionDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, match_id, session_id):
        try:
            match   = Match.objects.get(
                Q(pk=match_id) & (Q(user1=request.user) | Q(user2=request.user))
            )
            session = CollaborationSession.objects.get(pk=session_id, match=match)
        except (Match.DoesNotExist, CollaborationSession.DoesNotExist):
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CollaborationSessionSerializer(session, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, match_id, session_id):
        try:
            match   = Match.objects.get(
                Q(pk=match_id) & (Q(user1=request.user) | Q(user2=request.user))
            )
            session = CollaborationSession.objects.get(pk=session_id, match=match)
        except (Match.DoesNotExist, CollaborationSession.DoesNotExist):
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        session.delete()
        return Response(
            {'message': 'Session deleted.'},
            status=status.HTTP_204_NO_CONTENT,
        )


class CollaborationRatingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, match_id, session_id):
        try:
            match   = Match.objects.get(
                Q(pk=match_id) & (Q(user1=request.user) | Q(user2=request.user))
            )
            session = CollaborationSession.objects.get(
                pk=session_id,
                match=match,
                status=CollaborationSession.STATUS_COMPLETED,
            )
        except (Match.DoesNotExist, CollaborationSession.DoesNotExist):
            return Response(
                {'detail': 'Session not found or not completed yet.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        if CollaborationRating.objects.filter(session=session, rated_by=request.user).exists():
            return Response(
                {'detail': 'You have already rated this session.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        score = request.data.get('score')
        if not score or not (1 <= int(score) <= 5):
            return Response(
                {'detail': 'Score must be between 1 and 5.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        rated_user = match.other_user(request.user)
        rating = CollaborationRating.objects.create(
            session    = session,
            rated_by   = request.user,
            rated_user = rated_user,
            score      = int(score),
            review     = request.data.get('review', ''),
        )
        return Response(
            {'message': 'Rating submitted.', 'score': rating.score},
            status=status.HTTP_201_CREATED,
        )

    def get(self, request, match_id, session_id):
        try:
            match   = Match.objects.get(
                Q(pk=match_id) & (Q(user1=request.user) | Q(user2=request.user))
            )
            session = CollaborationSession.objects.get(pk=session_id, match=match)
        except (Match.DoesNotExist, CollaborationSession.DoesNotExist):
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        ratings = CollaborationRating.objects.filter(session=session)
        avg     = ratings.aggregate(avg=Avg('score'))['avg']
        return Response({
            'ratings': [
                {
                    'rated_by':   r.rated_by.email,
                    'rated_user': r.rated_user.email,
                    'score':      r.score,
                    'review':     r.review,
                    'created_at': r.created_at,
                }
                for r in ratings
            ],
            'average_score': round(avg, 1) if avg else None,
        })


class UserRatingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ratings = CollaborationRating.objects.filter(rated_user=request.user)
        avg     = ratings.aggregate(avg=Avg('score'))['avg']
        return Response({
            'average_score':  round(avg, 1) if avg else None,
            'total_ratings':  ratings.count(),
            'ratings': [
                {
                    'score':      r.score,
                    'review':     r.review,
                    'rated_by':   r.rated_by.email,
                    'created_at': r.created_at,
                }
                for r in ratings
            ],
        })