from .views import AdminLoginView, DisburseFundView, SendReminderView

from django.urls import path

urlpatterns = [
    path('login/', AdminLoginView.as_view(), name='admin-login'),
    path('disburse-fund/<int:contribution_id>/', DisburseFundView.as_view(), name='disburse-fund'),
    path('send-reminder/<int:contribution_id>/', SendReminderView.as_view(), name='send-reminder'),
]
