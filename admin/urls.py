from .views import AdminLoginView, DisburseFundView

from django.urls import path

urlpatterns = [
    path('login/', AdminLoginView.as_view(), name='admin-login'),
    path('disburse-fund/<int:contribution_id>/', DisburseFundView.as_view(), name='disburse-fund')
]
