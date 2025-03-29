from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from rest_framework.authtoken.models import Token

from .serializers import UserSerializer, LoginSerializer, RetrieveUserSerializer, ListUserSerializer, NotificationSerializer
from .models import User, Notification, NotificationType
from services.notification_service import NotificationService
from core.permissions import IsAuthenticated
from services.contriution_service import ContributionService


class ListCreateAPIView(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            amount = serializer.validated_data.get('contribution_amount')
            del serializer.validated_data['contribution_amount']
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)

            # create group for user
            ContributionService.add_member(user, amount)
            print("added")

            # send email notification
            NotificationService.send_email('Account Creation', f'Welcome {user.name},\n\nYou account has been successfully created for thrift contribution', user.email ) #'You have been paid an amount of ₦{{contribution.expected_amount}}.\nGroup name: {{group.name}}\nYour turn: {{user.group.position}}', user.email)
            
            return Response(
                status=HTTP_201_CREATED,
                data={
                    'status_code': HTTP_201_CREATED,
                    'message': 'User created successfully',
                    'data': {
                        'user': RetrieveUserSerializer(user).data,
                        'token': token.key
                    }
                },
        )
        return Response(
                status=HTTP_400_BAD_REQUEST,
                data={
                    'status_code': HTTP_400_BAD_REQUEST,
                    'message': 'Account creation failed',
                    'data': serializer.errors
                },
            )
        
    
    def list(self, request, *args, **kwargs):
        return Response(
            status=HTTP_200_OK,
            data={
                'status_code': HTTP_200_OK,
                'message': 'Users returned successfully',
                'data': ListUserSerializer(self.get_queryset(), many=True).data
            },
        )


class RetrieveUserView(RetrieveUpdateDestroyAPIView):
    serializer_class = RetrieveUserSerializer
    queryset = User.objects.all()
    
    def get(self, request, *args, **kwargs):
        user = self.get_object()
        return Response(
            status=HTTP_200_OK,
            data={
                'status_code': HTTP_200_OK,
                'message': 'User returned successfully',
                'data': RetrieveUserSerializer(user).data
            },
        )
    
    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = RetrieveUserSerializer(user, data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                status=HTTP_200_OK,
                data={
                    'status_code': HTTP_200_OK,
                    'message': 'User updated successfully',
                    'data': RetrieveUserSerializer(user).data
                },
            )
        return Response(
            status=HTTP_400_BAD_REQUEST,
            data={
                'status_code': HTTP_400_BAD_REQUEST,
                'message': 'User update failed',
                'data': serializer.errors
            },
        )
    
    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response(
            status=HTTP_200_OK,
            data={
                'status_code': HTTP_200_OK,
                'message': 'User deleted successfully',
                'data': RetrieveUserSerializer(user).data
            },
        )
    

class LoginView(CreateAPIView):
    serializer_class = LoginSerializer
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = None
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response(
                    status=HTTP_401_UNAUTHORIZED,
                    data={
                        'status_code': HTTP_401_UNAUTHORIZED,
                        'message': 'Incorrect email or password',
                        'data': None
                    },
                )
            if user.check_password(password):
                token, created = Token.objects.get_or_create(user=user)
                return Response(
                    status=HTTP_200_OK,
                    data={
                        'status_code': HTTP_200_OK,
                        'message': 'Login successful',
                        'data': {
                            'user': RetrieveUserSerializer(user).data,
                            'token': token.key
                        }
                    },
                )
            return Response(
                status=HTTP_401_UNAUTHORIZED,
                data={
                    'status_code': HTTP_401_UNAUTHORIZED,
                    'message': 'Invalid email or password',
                    'data': None
                },
            )
        return Response(
            status=HTTP_400_BAD_REQUEST,
            data={
                'status_code': HTTP_400_BAD_REQUEST,
                'message': 'Login failed',
                'data': serializer.errors
            },
        )
    


class NotificationListView(ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Notification.objects.all()


    def list(self, request, *args, **kwargs):
        return Response(
            status=HTTP_200_OK,
            data={
                'message': 'Notifications',
                'data': NotificationSerializer(request.user.notifications.all(), many=True).data,
                'status_code': HTTP_200_OK
            }
        )