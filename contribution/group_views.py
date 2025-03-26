from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from rest_framework.authentication import TokenAuthentication
import datetime

from .serializers import GroupSerializer, UserGroupSerializer
from .models import Group, UserGroup, Contribution, ContributionStatus
from core.permissions import IsAdmin, IsAuthenticated
from core.constants import MAX_GROUP_USERS
from utils.date_utils import DateUtil



class ListCreateGroupView(ListCreateAPIView):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    permission_classes = (IsAuthenticated, IsAdmin,)
    
    def post(self, request, *args, **kwargs):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            group = serializer.save()

            # create contributions
            for i in range(1, MAX_GROUP_USERS+1):
                start_date = DateUtil.get_date(i-1)[0]
                end_date = DateUtil.get_date(i-1)[1]

                Contribution.objects.get_or_create(
                    group=group, position=i, defaults={'payout_to': None, 'amount': group.contribution_amount, 'start_date': start_date, 'end_date': end_date}
                )

            # set rotation for users
            for contribution, user in zip(group.contributions.all(), group.users.all()):
                contribution.payout_to = user
                contribution.save()

            return Response(
                status=HTTP_201_CREATED,
                data={
                    'status_code': HTTP_201_CREATED,
                    'message': 'Group created successfully',
                    'data': GroupSerializer(group).data
                },
            )
        return Response(
            status=HTTP_400_BAD_REQUEST,
            data={
                'status_code': HTTP_400_BAD_REQUEST,
                'message': 'Group creation failed',
                'data': serializer.errors
            },
        )
        
    
    def list(self, request, *args, **kwargs):
        return Response(
            status=HTTP_200_OK,
            data={
                'status_code': HTTP_200_OK,
                'message': 'Groups returned successfully',
                'data': GroupSerializer(self.get_queryset(), many=True).data
            },
        )

class RetrieveGroupView(RetrieveUpdateDestroyAPIView):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    
    def get(self, request, *args, **kwargs):
        group = self.get_object()
        return Response(
            status=HTTP_200_OK,
            data={
                'status_code': HTTP_200_OK,
                'message': 'Group returned successfully',
                'data': GroupSerializer(group).data
            },
       )
    
    def update(self, request, *args, **kwargs):
        group = self.get_object()
        serializer = GroupSerializer(group, data=request.data)
        if serializer.is_valid():
            group = serializer.save()
            return Response(
                status=HTTP_200_OK,
                data={
                    'status_code': HTTP_200_OK,
                    'message': 'Group updated successfully',
                    'data': GroupSerializer(group).data
                },
            )
        return Response(
            status=HTTP_400_BAD_REQUEST,
            data={
                'status_code': HTTP_400_BAD_REQUEST,
                'message': 'Group update failed',
                'data': serializer.errors
            },
        )
    
    def delete(self, request, *args, **kwargs):
        group = self.get_object()
        group.delete()
        return Response(
            status=HTTP_200_OK,
            data={
                'status_code': HTTP_200_OK,
                'message': 'Group deleted successfully',
                'data': None
            },
        )
    

class ListGroupUserView(ListAPIView):
    serializer_class = UserGroupSerializer
    queryset = UserGroup.objects.all()
    
    def list(self, request, *args, **kwargs):
        try:
            group = Group.objects.get(id=kwargs.get('group_id'))
            return Response(
                status=HTTP_200_OK,
                data={
                    'status_code': HTTP_200_OK,
                    'message': 'Group users returned successfully',
                    'data': UserGroupSerializer(group.users, many=True).data
                },
            )
        except Group.DoesNotExist:
            return Response(
                status=HTTP_404_NOT_FOUND,
                data={
                    'status_code': HTTP_404_NOT_FOUND,
                    'message': 'Group not found',
                    'error': 'Group not found'
                },
            )

class AddUserToGroupView(CreateAPIView):
    queryset = UserGroup.objects.all()
    serializer_class = UserGroupSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdmin)
    
    def post(self, request, *args, **kwargs):
        serializer = UserGroupSerializer(data=request.data)
        if serializer.is_valid():
            user_group = serializer.save()

            # set rotation for users
            for contribution, user in zip(user_group.group.contributions.all(), user_group.group.users.all()):
                if contribution.position == user_group.position:
                    contribution.payout_to = user.user

                    if contribution.position != 1: # other contributions should be inactive
                        contribution.status = ContributionStatus.INACTIVE
                        
                    contribution.save()

            return Response(
                status=HTTP_201_CREATED,
                data={
                    'status_code': HTTP_201_CREATED,
                    'message': 'User added to group successfully',
                    'data': UserGroupSerializer(user_group).data
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
