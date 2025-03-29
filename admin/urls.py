from .views import AdminLoginView, DisburseFundView, SendReminderView, AdminDashboardView, PayoutScheduleView

from django.urls import path

urlpatterns = [
    path('login/', AdminLoginView.as_view(), name='admin-login'),
    path('disburse-fund/<int:contribution_id>/', DisburseFundView.as_view(), name='disburse-fund'),
    path('send-reminder/<int:contribution_id>/', SendReminderView.as_view(), name='send-reminder'),
    path('analytics-data/', AdminDashboardView.as_view(), name='analytics'),
    path('payout-schedule/<int:group_id>/', PayoutScheduleView.as_view(), name='payout-schedule'),
]
