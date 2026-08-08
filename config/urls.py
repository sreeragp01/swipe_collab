from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from config.views import translate_view

urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/v1/translate/',     translate_view, name='translate_api'),
    path('api/v1/auth/',          include('users.urls')),
    path('api/v1/profiles/',      include('profiles.urls')),
    path('api/v1/swipe/',         include('swipe.urls')),
    path('api/v1/matches/',       include('matches.urls')),
    path('api/v1/chat/',          include('chat.urls')),
    path('api/v1/projects/',      include('projects.urls')),
    path('api/v1/invitations/',   include('invitations.urls')),
    path('api/v1/workspaces/',    include('workspaces.urls')),
    path('api/v1/reviews/',       include('reviews.urls')),
    path('api/v1/payments/',      include('payments.urls')),
    path('api/v1/moderation/',    include('moderation.urls')),
    path('api/v1/analytics/',     include('analytics.urls')),
    path('api/v1/notifications/', include('notifications.urls')),
    path('api/v1/superadmin/',    include('superadmin.urls')),

    # Frontend HTML pages
    path('',              TemplateView.as_view(template_name='index.html'),          name='index'),
    path('login/',        TemplateView.as_view(template_name='login.html'),          name='login'),
    path('register/',     TemplateView.as_view(template_name='register.html'),       name='register'),
    path('dashboard/',    TemplateView.as_view(template_name='dashboard.html'),      name='dashboard'),
    path('discover/',     TemplateView.as_view(template_name='discover.html'),       name='discover'),
    path('project-detail/', TemplateView.as_view(template_name='project_detail.html'), name='project-detail-page'),
    path('talent/',       TemplateView.as_view(template_name='talent.html'),         name='talent'),
    path('workspace/',    TemplateView.as_view(template_name='workspace.html'),      name='workspace'),
    path('profile/',      TemplateView.as_view(template_name='profile.html'),        name='profile'),
    path('profile-view/', TemplateView.as_view(template_name='profile_view.html'),   name='profile-view'),
    path('swipe/',        TemplateView.as_view(template_name='swipe.html'),          name='swipe'),
    path('matches/',      TemplateView.as_view(template_name='matches.html'),        name='matches'),
    path('chat/',         TemplateView.as_view(template_name='chat.html'),           name='chat'),
    path('projects/',     TemplateView.as_view(template_name='projects.html'),       name='projects'),
    path('payment/',      TemplateView.as_view(template_name='payment.html'),        name='payment'),
    path('moderation/',   TemplateView.as_view(template_name='moderation.html'),     name='moderation'),
    path('superadmin/',   TemplateView.as_view(template_name='superadmin.html'),     name='superadmin'),
    path('verify-email/', TemplateView.as_view(template_name='verify_email.html'),   name='verify-email'),
    path('settings/',     TemplateView.as_view(template_name='settings.html'),       name='settings'),
    path('portfolio-show/', TemplateView.as_view(template_name='portfolio_show.html'), name='portfolio-show'),
]

# Serve media and static files with caching headers
from django.views.static import serve
from django.urls import re_path

def cached_static_serve(request, path, document_root=None, show_indexes=False):
    response = serve(request, path, document_root=document_root, show_indexes=show_indexes)
    if response.status_code == 200:
        response['Cache-Control'] = 'public, max-age=86400'
    return response

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^css/(?P<path>.*)$', cached_static_serve, {'document_root': settings.BASE_DIR / 'frontend' / 'css'}),
    re_path(r'^js/(?P<path>.*)$', cached_static_serve, {'document_root': settings.BASE_DIR / 'frontend' / 'js'}),
    re_path(r'^static/css/(?P<path>.*)$', cached_static_serve, {'document_root': settings.BASE_DIR / 'frontend' / 'css'}),
    re_path(r'^static/js/(?P<path>.*)$', cached_static_serve, {'document_root': settings.BASE_DIR / 'frontend' / 'js'}),
]