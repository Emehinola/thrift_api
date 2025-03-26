from django.urls import path

from .group_views import ListCreateGroupView, RetrieveGroupView, ListGroupUserView, AddUserToGroupView

urlpatterns = [
    path('', ListCreateGroupView.as_view(), name='groups'),
    path('<int:pk>/', RetrieveGroupView.as_view(), name='group'),
    path('<int:group_id>/users', ListGroupUserView.as_view(), name='group-users'),
    path('users/add', AddUserToGroupView.as_view(), name='group-add-user'),
]
