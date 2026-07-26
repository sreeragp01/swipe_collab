from django.urls import path
from .views import (
    SkillListView,
    FreelancerProfileMeView,
    FreelancerProfileDetailView,
    FreelancerProfileListView,
    FreelancerProfileByUserView,
    CompanyProfileMeView,
    CompanyProfileDetailView,
    CompanyProfileListView,
    CompanyProfileByUserView,
    PortfolioItemView,
    PortfolioItemDetailView,
    PortfolioItemLikeToggleView,
    PortfolioItemCommentView,
)

urlpatterns = [
    path('skills/',                         SkillListView.as_view(),                name='skill-list'),

    path('freelancer/me/',                  FreelancerProfileMeView.as_view(),      name='freelancer-me'),
    path('freelancer/',                     FreelancerProfileListView.as_view(),    name='freelancer-list'),
    path('freelancer/<int:pk>/',            FreelancerProfileDetailView.as_view(),  name='freelancer-detail'),
    path('freelancer/by-user/<str:uid>/',   FreelancerProfileByUserView.as_view(),  name='freelancer-by-user'),

    path('company/me/',                     CompanyProfileMeView.as_view(),         name='company-me'),
    path('company/',                        CompanyProfileListView.as_view(),       name='company-list'),
    path('company/<int:pk>/',               CompanyProfileDetailView.as_view(),     name='company-detail'),
    path('company/by-user/<str:uid>/',      CompanyProfileByUserView.as_view(),     name='company-by-user'),

    path('portfolio/',                      PortfolioItemView.as_view(),            name='portfolio-item-list'),
    path('portfolio/<int:pk>/',             PortfolioItemDetailView.as_view(),      name='portfolio-item-detail'),
    path('portfolio/<int:pk>/like/',        PortfolioItemLikeToggleView.as_view(),  name='portfolio-item-like'),
    path('portfolio/<int:pk>/comment/',     PortfolioItemCommentView.as_view(),     name='portfolio-item-comment'),
]