from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/v1/auth/',       include('users.urls')),
    path('api/v1/profiles/',   include('profiles.urls')),
    path('api/v1/swipe/',      include('swipe.urls')),
    path('api/v1/matches/',    include('matches.urls')),
    path('api/v1/chat/',       include('chat.urls')),
    path('api/v1/projects/',   include('projects.urls')),
    path('api/v1/payments/',   include('payments.urls')),
    path('api/v1/moderation/', include('moderation.urls')),
    path('api/v1/analytics/',  include('analytics.urls')),
    path('api/v1/notifications/', include('notifications.urls')),

    # Frontend HTML pages
    path('',              TemplateView.as_view(template_name='index.html'),        name='index'),
    path('login/',        TemplateView.as_view(template_name='login.html'),        name='login'),
    path('register/',     TemplateView.as_view(template_name='register.html'),     name='register'),
    path('dashboard/',    TemplateView.as_view(template_name='dashboard.html'),    name='dashboard'),
    path('profile/',      TemplateView.as_view(template_name='profile.html'),      name='profile'),
    path('profile-view/', TemplateView.as_view(template_name='profile_view.html'), name='profile-view'),
    path('swipe/',        TemplateView.as_view(template_name='swipe.html'),        name='swipe'),
    path('matches/',      TemplateView.as_view(template_name='matches.html'),      name='matches'),
    path('chat/',         TemplateView.as_view(template_name='chat.html'),         name='chat'),
    path('projects/',     TemplateView.as_view(template_name='projects.html'),     name='projects'),
    path('payment/',      TemplateView.as_view(template_name='payment.html'),      name='payment'),
    path('moderation/',   TemplateView.as_view(template_name='moderation.html'),   name='moderation'),
    path('verify-email/', TemplateView.as_view(template_name='verify_email.html'), name='verify-email'),
    path('settings/',     TemplateView.as_view(template_name='settings.html'),     name='settings'),
    path('portfolio-show/', TemplateView.as_view(template_name='portfolio_show.html'), name='portfolio-show'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)