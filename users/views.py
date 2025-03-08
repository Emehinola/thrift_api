from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from .serializers import UserSerializer, LoginSerializer, RetrieveUserSerializer
from .models import User


class ListCreateAPIView(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                status=HTTP_201_CREATED,
                data={
                    'status_code': HTTP_201_CREATED,
                    'message': 'User created successfully',
                    'data': UserSerializer(user).data
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
                'data': UserSerializer(self.get_queryset(), many=True).data
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