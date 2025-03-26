from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from .serializers import ContributionSerializer

from .models import Contribution


class ContributionView(ListAPIView):
    serializer_class = ContributionSerializer
    queryset = Contribution.objects.all()
    
    def list(self, request, *args, **kwargs):
        return Response(
            status=HTTP_200_OK,
            data={
                'status_code': HTTP_200_OK,
                'message': 'Contributions returned successfully',
                'data': ContributionSerializer(self.get_queryset(), many=True).data
            },
        )