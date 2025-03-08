from .views import ListCreateAPIView, RetrieveUserView

from django.urls import path

urlpatterns = [
    path('', ListCreateAPIView.as_view(), name='users'),
    path('<int:pk>/', RetrieveUserView.as_view(), name='user')
]
