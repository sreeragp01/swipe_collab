from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import Skill, FreelancerProfile, CompanyProfile, PortfolioItem, PortfolioItemLike, PortfolioItemComment
from .serializers import (
    SkillSerializer,
    FreelancerProfileSerializer,
    FreelancerProfileCardSerializer,
    CompanyProfileSerializer,
    CompanyProfileCardSerializer,
    PortfolioItemSerializer,
    PortfolioItemCommentSerializer,
)


class SkillListView(generics.ListCreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Skill.objects.all()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__icontains=category)
        return queryset

    def create(self, request, *args, **kwargs):
        name = request.data.get('name', '').strip()
        if not name:
            return Response({'detail': 'Skill name is required.'}, status=status.HTTP_400_BAD_REQUEST)
        skill, created = Skill.objects.get_or_create(
            name__iexact=name,
            defaults={'name': name, 'category': request.data.get('category', 'Custom')}
        )
        serializer = self.get_serializer(skill)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class FreelancerProfileMeView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):
        try:
            profile = request.user.freelancer_profile
            serializer = FreelancerProfileSerializer(profile)
            return Response(serializer.data)
        except FreelancerProfile.DoesNotExist:
            return Response({'detail': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        if not request.user.is_freelancer:
            return Response({'detail': 'Only freelancers can create a freelancer profile.'}, status=status.HTTP_403_FORBIDDEN)
        if FreelancerProfile.objects.filter(user=request.user).exists():
            return Response({'detail': 'Profile already exists. Use PATCH to update.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = FreelancerProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        try:
            profile = request.user.freelancer_profile
        except FreelancerProfile.DoesNotExist:
            return Response({'detail': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = FreelancerProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            profile = request.user.freelancer_profile
            profile.delete()
            return Response({'message': 'Profile deleted.'}, status=status.HTTP_204_NO_CONTENT)
        except FreelancerProfile.DoesNotExist:
            return Response({'detail': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)


class FreelancerProfileDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            profile = FreelancerProfile.objects.get(pk=pk)
            serializer = FreelancerProfileCardSerializer(profile)
            return Response(serializer.data)
        except FreelancerProfile.DoesNotExist:
            return Response({'detail': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)


class FreelancerProfileListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FreelancerProfileCardSerializer

    def get_queryset(self):
        queryset = FreelancerProfile.objects.all()
        skill = self.request.query_params.get('skill')
        availability = self.request.query_params.get('availability')
        country = self.request.query_params.get('country')
        exp_min = self.request.query_params.get('exp_min')
        exp_max = self.request.query_params.get('exp_max')

        if skill:
            queryset = queryset.filter(skills__name__icontains=skill)
        if availability:
            queryset = queryset.filter(availability=availability)
        if country:
            queryset = queryset.filter(country__icontains=country)
        if exp_min:
            queryset = queryset.filter(experience_years__gte=exp_min)
        if exp_max:
            queryset = queryset.filter(experience_years__lte=exp_max)

        return queryset.distinct()


class CompanyProfileMeView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):
        try:
            profile = request.user.company_profile
            serializer = CompanyProfileSerializer(profile)
            return Response(serializer.data)
        except CompanyProfile.DoesNotExist:
            return Response({'detail': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        if not request.user.is_company:
            return Response({'detail': 'Only companies can create a company profile.'}, status=status.HTTP_403_FORBIDDEN)
        if CompanyProfile.objects.filter(user=request.user).exists():
            return Response({'detail': 'Profile already exists. Use PATCH to update.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CompanyProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        try:
            profile = request.user.company_profile
        except CompanyProfile.DoesNotExist:
            return Response({'detail': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CompanyProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            profile = request.user.company_profile
            profile.delete()
            return Response({'message': 'Profile deleted.'}, status=status.HTTP_204_NO_CONTENT)
        except CompanyProfile.DoesNotExist:
            return Response({'detail': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)


class CompanyProfileDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            profile = CompanyProfile.objects.get(pk=pk)
            serializer = CompanyProfileCardSerializer(profile)
            return Response(serializer.data)
        except CompanyProfile.DoesNotExist:
            return Response({'detail': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)


class CompanyProfileListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CompanyProfileCardSerializer

    def get_queryset(self):
        queryset = CompanyProfile.objects.all()
        skill = self.request.query_params.get('skill')
        country = self.request.query_params.get('country')

        if skill:
            queryset = queryset.filter(skills__name__icontains=skill)
        if country:
            queryset = queryset.filter(country__icontains=country)

        return queryset.distinct()


class FreelancerProfileByUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, uid):
        try:
            profile = FreelancerProfile.objects.get(user__id=uid)
            serializer = FreelancerProfileSerializer(profile)
            return Response(serializer.data)
        except FreelancerProfile.DoesNotExist:
            return Response({'detail': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)


class CompanyProfileByUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, uid):
        try:
            profile = CompanyProfile.objects.get(user__id=uid)
            serializer = CompanyProfileSerializer(profile)
            return Response(serializer.data)
        except CompanyProfile.DoesNotExist:
            return Response({'detail': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)


class PortfolioItemView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):
        if not request.user.is_freelancer:
            return Response([])
        try:
            profile = request.user.freelancer_profile
            items = profile.portfolio_items.all()
            return Response(PortfolioItemSerializer(items, many=True).data)
        except FreelancerProfile.DoesNotExist:
            return Response([])

    def post(self, request):
        if not request.user.is_freelancer:
            return Response({'detail': 'Only freelancers can add portfolio items.'}, status=status.HTTP_403_FORBIDDEN)
        try:
            profile = request.user.freelancer_profile
        except FreelancerProfile.DoesNotExist:
            return Response({'detail': 'Create a freelancer profile first.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PortfolioItemSerializer(data=request.data)
        if serializer.is_valid():
            item = serializer.save(freelancer=profile)
            return Response(PortfolioItemSerializer(item).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PortfolioItemDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        if not request.user.is_freelancer:
            return Response({'detail': 'Forbidden.'}, status=status.HTTP_403_FORBIDDEN)
        try:
            item = PortfolioItem.objects.get(pk=pk, freelancer__user=request.user)
            item.delete()
            return Response({'message': 'Portfolio item deleted.'}, status=status.HTTP_204_NO_CONTENT)
        except PortfolioItem.DoesNotExist:
            return Response({'detail': 'Not found or not yours.'}, status=status.HTTP_404_NOT_FOUND)


class PortfolioItemLikeToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            item = PortfolioItem.objects.get(pk=pk)
        except PortfolioItem.DoesNotExist:
            return Response({'detail': 'Portfolio item not found.'}, status=status.HTTP_404_NOT_FOUND)

        like_qs = PortfolioItemLike.objects.filter(item=item, user=request.user)
        if like_qs.exists():
            like_qs.delete()
            liked = False
        else:
            PortfolioItemLike.objects.create(item=item, user=request.user)
            liked = True
            if item.freelancer.user != request.user:
                try:
                    from notifications.models import notify_user, Notification
                    notify_user(
                        user=item.freelancer.user,
                        sender=request.user,
                        notification_type=Notification.TYPE_PORTFOLIO_LIKE,
                        title="Project Liked ❤️",
                        message=f"{request.user.full_name} liked your showcase project '{item.title}'.",
                        link=f"/profile-view/?id={item.freelancer.user.id}",
                    )
                except Exception:
                    pass

        return Response({
            'liked': liked,
            'like_count': item.likes.count(),
        })


class PortfolioItemCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            item = PortfolioItem.objects.get(pk=pk)
        except PortfolioItem.DoesNotExist:
            return Response({'detail': 'Portfolio item not found.'}, status=status.HTTP_404_NOT_FOUND)

        text = request.data.get('text', '').strip()
        if not text:
            return Response({'detail': 'Comment text is required.'}, status=status.HTTP_400_BAD_REQUEST)

        comment = PortfolioItemComment.objects.create(
            item=item,
            user=request.user,
            text=text,
        )

        if item.freelancer.user != request.user:
            try:
                from notifications.models import notify_user, Notification
                notify_user(
                    user=item.freelancer.user,
                    sender=request.user,
                    notification_type=Notification.TYPE_PORTFOLIO_COMMENT,
                    title="New Comment on Project 💬",
                    message=f"{request.user.full_name} commented on '{item.title}': {text[:40]}",
                    link=f"/profile-view/?id={item.freelancer.user.id}",
                )
            except Exception:
                pass

        serializer = PortfolioItemCommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)