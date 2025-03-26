from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from rest_framework.authtoken.models import Token

from users.serializers import UserSerializer, LoginSerializer, RetrieveUserSerializer
from users.models import User



class AdminLoginView(CreateAPIView):
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
            if not user.is_admin:
                return Response(
                    status=HTTP_401_UNAUTHORIZED,
                    data={
                        'status_code': HTTP_401_UNAUTHORIZED,
                        'message': 'Only admin login is allowed',
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
    


class AddMemberToGroupView(CreateAPIView):
    serializer_class = UserSerializer
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            user = None
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response(
                    status=HTTP_404_NOT_FOUND,
                    data={
                        'status_code': HTTP_404_NOT_FOUND,
                        'message': 'User not found',
                        'data': None
                    },
                )
            user.groups.add(kwargs.get('group_id'))
            return Response(
                status=HTTP_200_OK,
                data={
                    'status_code': HTTP_200_OK,
                    'message': 'User added to group successfully',
                    'data': RetrieveUserSerializer(user).data
                },
            )
        return Response(
            status=HTTP_400_BAD_REQUEST,
            data={
                'status_code': HTTP_400_BAD_REQUEST,
                'message': 'User addition to group failed',
                'data': serializer.errors
            },
        )