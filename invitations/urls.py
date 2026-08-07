from django.urls import path
from invitations.views import (
    InvitationListCreateView,
    ReceivedInvitationsListView,
    RespondInvitationView,
)

urlpatterns = [
    path('', InvitationListCreateView.as_view(), name='invitation-list-create'),
    path('received/', ReceivedInvitationsListView.as_view(), name='received-invitations'),
    path('<int:pk>/respond/', RespondInvitationView.as_view(), name='respond-invitation'),
]
