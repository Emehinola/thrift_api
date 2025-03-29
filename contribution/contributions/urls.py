from .views import ListContributionView, RetrieveContributionByGroupView, RetrieveContributionForUserView, GetReceiptView

from django.urls import path

urlpatterns = [
    path('', ListContributionView.as_view(), name='contributions'),
    path('<int:group_id>/', RetrieveContributionByGroupView.as_view(), name='contribution'),
    path('<int:group_id>/self/', RetrieveContributionForUserView.as_view(), name='contributions-self'),\
    path('receipt/<contribution_id>/', GetReceiptView.as_view(), name='receipt'),
]
