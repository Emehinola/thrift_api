from django.urls import path

from .views import ListDashboardGroupView

urlpatterns = [
    path('groups/', ListDashboardGroupView.as_view(), name='dashboard-groups'),
]
