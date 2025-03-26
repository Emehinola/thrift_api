from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from ..models import Group
from ..serializers import DashboardGroupSerializer


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