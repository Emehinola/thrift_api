from django.urls import path

from .views import FundContributionView

urlpatterns = [
    path('fund-contribution/', FundContributionView.as_view(), name='fund-contribution')
]
