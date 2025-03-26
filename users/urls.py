from .views import ListCreateAPIView, RetrieveUserView, LoginView

from django.urls import path

urlpatterns = [
    path('', ListCreateAPIView.as_view(), name='users'),
    path('<int:pk>/', RetrieveUserView.as_view(), name='user'),
    path('login/', LoginView.as_view(), name='login')
]
