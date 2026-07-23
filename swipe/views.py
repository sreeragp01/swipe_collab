from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings

from matches.models import Match
from profiles.models import FreelancerProfile, CompanyProfile
from profiles.serializers import FreelancerProfileCardSerializer, CompanyProfileCardSerializer
from .models import SwipeAction, SwipeFilter, SkillMatchScore
from .serializers import SwipeActionSerializer, SwipeFilterSerializer

User = get_user_model()


def attach_skill_scores(profiles, user, id_field='user_id'):
    scores = {
        s.target_id: s.score
        for s in SkillMatchScore.objects.filter(user=user)
    }
    result = []
    for p in profiles:
        data = p if isinstance(p, dict) else p.__dict__
        target_id = getattr(p, 'user_id', None) if not isinstance(p, dict) else p.get('user', {}).get('id')
        score = scores.get(target_id, None)
        result.append({'profile': p, 'skill_match_score': score})
    return result


class SwipeFeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user


        TESTING_MODE = getattr(settings, 'TESTING_MODE', False)

        if not TESTING_MODE and not user.can_swipe:
            return Response(
                {'detail': 'You must be verified and have an active plan to swipe.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        already_swiped = SwipeAction.objects.filter(swiper=user).values_list('target_id', flat=True)
        blocked = user.blocked_users.values_list('blocked_id', flat=True)
        blocked_by = user.blocked_by_users.values_list('blocker_id', flat=True)
        exclude_ids = set(already_swiped) | set(blocked) | set(blocked_by) | {user.id}

        try:
            swipe_filter = SwipeFilter.objects.filter(user=user).latest('updated_at')
        except SwipeFilter.DoesNotExist:
            swipe_filter = None

        super_likes_left = 3 - SwipeAction.super_likes_used_today(user)

        if user.is_freelancer:
            queryset = CompanyProfile.objects.exclude(user_id__in=exclude_ids)
            if swipe_filter:
                if swipe_filter.country:
                    queryset = queryset.filter(country__icontains=swipe_filter.country)
                if swipe_filter.city:
                    queryset = queryset.filter(city__icontains=swipe_filter.city)
                if swipe_filter.required_skills.exists():
                    queryset = queryset.filter(skills__in=swipe_filter.required_skills.all()).distinct()
            profiles = queryset[:20]
            serialized = CompanyProfileCardSerializer(profiles, many=True).data

            scores = {
                str(s.target_id): s.score
                for s in SkillMatchScore.objects.filter(user=user, target_id__in=[p.user_id for p in profiles])
            }
            feed = []
            for i, p in enumerate(profiles):
                card = dict(serialized[i])
                card['skill_match_score'] = scores.get(str(p.user_id))
                feed.append(card)
        else:
            queryset = FreelancerProfile.objects.exclude(user_id__in=exclude_ids)
            if swipe_filter:
                if swipe_filter.experience_min:
                    queryset = queryset.filter(experience_years__gte=swipe_filter.experience_min)
                if swipe_filter.experience_max:
                    queryset = queryset.filter(experience_years__lte=swipe_filter.experience_max)
                if swipe_filter.country:
                    queryset = queryset.filter(country__icontains=swipe_filter.country)
                if swipe_filter.city:
                    queryset = queryset.filter(city__icontains=swipe_filter.city)
                if swipe_filter.availability:
                    queryset = queryset.filter(availability=swipe_filter.availability)
                if swipe_filter.required_skills.exists():
                    queryset = queryset.filter(skills__in=swipe_filter.required_skills.all()).distinct()
            profiles = queryset[:20]
            serialized = FreelancerProfileCardSerializer(profiles, many=True).data

            scores = {
                str(s.target_id): s.score
                for s in SkillMatchScore.objects.filter(user=user, target_id__in=[p.user_id for p in profiles])
            }
            feed = []
            for i, p in enumerate(profiles):
                card = dict(serialized[i])
                card['skill_match_score'] = scores.get(str(p.user_id))
                feed.append(card)

        return Response({
            'feed': feed,
            'count': len(feed),
            'super_likes_remaining': super_likes_left,
        })


class SwipeActionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user


        TESTING_MODE = getattr(settings, 'TESTING_MODE', False)

        if not TESTING_MODE and not user.can_swipe:
            return Response(
                {'detail': 'You must be verified and have an active plan to swipe.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        target_id = request.data.get('target_id')
        action = request.data.get('action')

        if not target_id or not action:
            return Response({'detail': 'target_id and action are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if action not in [SwipeAction.ACTION_LIKE, SwipeAction.ACTION_PASS, SwipeAction.ACTION_SUPER_LIKE]:
            return Response({'detail': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)

        if action == SwipeAction.ACTION_SUPER_LIKE and not SwipeAction.can_super_like(user):
            used = SwipeAction.super_likes_used_today(user)
            return Response({
                'detail': f'Super like daily limit reached. You have used {used}/3 today.',
                'super_likes_remaining': 0,
            }, status=status.HTTP_429_TOO_MANY_REQUESTS)

        try:
            target = User.objects.get(id=target_id)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if target == user:
            return Response({'detail': 'You cannot swipe on yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        swipe, created = SwipeAction.objects.get_or_create(
            swiper=user,
            target=target,
            defaults={'action': action},
        )

        if not created:
            return Response({'detail': 'You have already swiped on this user.'}, status=status.HTTP_400_BAD_REQUEST)

        score = SkillMatchScore.calculate(user, target)
        SkillMatchScore.objects.update_or_create(
            user=user, target=target,
            defaults={'score': score},
        )

        response_data = {
            'action': action,
            'matched': False,
            'skill_match_score': score,
            'super_likes_remaining': 3 - SwipeAction.super_likes_used_today(user),
        }

        if action in [SwipeAction.ACTION_LIKE, SwipeAction.ACTION_SUPER_LIKE]:
            if SwipeAction.is_mutual_like(user, target):
                match = Match.create(user, target)
                from chat.models import ChatRoom
                ChatRoom.objects.create(match=match)
                response_data['matched'] = True
                response_data['match_id'] = match.id
                response_data['hours_to_send_message'] = 48

                try:
                    stats = user.engagement_stats
                    stats.increment('match_count')
                except Exception:
                    pass

            try:
                stats = user.engagement_stats
                stats.increment('total_swipes_made')
            except Exception:
                pass

            try:
                target_stats = target.engagement_stats
                target_stats.increment('total_likes_received')
            except Exception:
                pass

        return Response(response_data, status=status.HTTP_201_CREATED)


class WhoLikedMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        TESTING_MODE = getattr(settings, 'TESTING_MODE', False)

        if not TESTING_MODE and not user.can_swipe:
            return Response(
                {'detail': 'You must be verified and have an active plan to view who liked you.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Only exclude people the current user has ALREADY liked back (mutual like = they're in Matches)
        # Passes don't hide an interest - the person still showed interest
        liked_back_by_me = SwipeAction.objects.filter(
            swiper=user,
            action__in=[SwipeAction.ACTION_LIKE, SwipeAction.ACTION_SUPER_LIKE],
        ).values_list('target_id', flat=True)

        likes = SwipeAction.objects.filter(
            target=user,
            action__in=[SwipeAction.ACTION_LIKE, SwipeAction.ACTION_SUPER_LIKE],
        ).exclude(swiper_id__in=liked_back_by_me).select_related('swiper')

        data = []
        for s in likes:
            swiper = s.swiper
            score = SkillMatchScore.calculate(user, swiper)
            profile_data = None
            role = 'freelancer' if swiper.is_freelancer else 'company'
            try:
                if swiper.is_freelancer and hasattr(swiper, 'freelancer_profile'):
                    profile_data = FreelancerProfileCardSerializer(swiper.freelancer_profile).data
                elif hasattr(swiper, 'company_profile'):
                    profile_data = CompanyProfileCardSerializer(swiper.company_profile).data
            except Exception:
                profile_data = None

            data.append({
                'user_id': str(swiper.id),
                'email': swiper.email,
                'role': role,
                'action': s.action,
                'liked_at': s.created_at,
                'skill_match_score': score,
                'profile': profile_data,
            })

        return Response({'liked_by': data, 'count': len(data)})



class SwipeFilterView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            swipe_filter = SwipeFilter.objects.filter(user=request.user).latest('updated_at')
            serializer = SwipeFilterSerializer(swipe_filter)
            return Response(serializer.data)
        except SwipeFilter.DoesNotExist:
            return Response({})

    def post(self, request):
        serializer = SwipeFilterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        try:
            swipe_filter = SwipeFilter.objects.filter(user=request.user).latest('updated_at')
        except SwipeFilter.DoesNotExist:
            return Response({'detail': 'No filter found. Use POST to create one.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = SwipeFilterSerializer(swipe_filter, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)