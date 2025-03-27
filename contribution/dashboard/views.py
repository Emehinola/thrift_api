from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from ..models import Group
from ..serializers import DashboardGroupSerializer, UserDashboardSerializer
from core.permissions import IsAuthenticated


class ListDashboardGroupView(ListAPIView):
    serializer_class = DashboardGroupSerializer
    queryset = Group.objects.all()
    
    def list(self, request, *args, **kwargs):
        return Response(
            status=HTTP_200_OK,
            data={
                'status_code': HTTP_200_OK,
                'message': 'Groups returned successfully',
                'data': DashboardGroupSerializer(self.get_queryset(), many=True).data
            },
        )
    

class UserDashboardView(RetrieveAPIView):
    serializer_class = UserDashboardSerializer
    permission_classes = (IsAuthenticated,)


    def retrieve(self, request, *args, **kwargs):
        user = request.user
        return Response(
            status=HTTP_200_OK,
            data={
                'status_code': HTTP_200_OK,
                'message': 'User dashboard returned successfully',
                'data': UserDashboardSerializer(user, context={'user':request.user}).data
            },
        )