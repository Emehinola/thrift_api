from django.urls import path

from .views import ListDashboardGroupView, UserDashboardView

urlpatterns = [
    path('groups/', ListDashboardGroupView.as_view(), name='dashboard-groups'),
    path('user-data/', UserDashboardView.as_view(), name='dashboard-user-data'),
]
