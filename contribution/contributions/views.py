from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import response, status

from ..serializers import AdminContributionSerializer, SelfContributionSerializer
from ..models import Contribution, Group
from core.permissions import IsStrictlyAuthenticated, IsAuthenticated
from services.notification_service import NotificationService


class ListContributionView(ListAPIView):
    serializer_class = AdminContributionSerializer
    queryset = Contribution.objects.all()

    def list(self, request, *args, **kwargs):
        return response.Response(
            data={
                'status_code': status.HTTP_200_OK,
                'message': 'Contributions returned',
                'data': AdminContributionSerializer(self.get_queryset(), many=True).data
            },
            status=status.HTTP_200_OK
        )
    

class RetrieveContributionByGroupView(RetrieveAPIView):
    serializer_class = AdminContributionSerializer
    queryset = Contribution.objects.all()

    def retrieve(self, request, *args, **kwargs):
        try:
            group = Group.objects.get(id=kwargs.get('group_id'))
            return response.Response(
                data={
                    'status_code': status.HTTP_200_OK,
                    'message': 'Contribution returned',
                    'data': AdminContributionSerializer(group.contributions.all(), many=True).data
                },
                status=status.HTTP_200_OK
            )
        except:
            return response.Response(
                data={
                    'status_code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Failed to get contributions',
                    'error': 'Failed to get contributions'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
class RetrieveContributionForUserView(RetrieveAPIView):
    serializer_class = SelfContributionSerializer
    queryset = Contribution.objects.all()
    permission_classes = (IsStrictlyAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        try:
            group = Group.objects.get(id=kwargs.get('group_id'))
            user = request.user
            contributions = group.contributions.filter(group=group)
            return response.Response(
                data={
                    'status_code': status.HTTP_200_OK,
                    'message': 'Contribution returned',
                    'data': SelfContributionSerializer(contributions, many=True, context={'user': user}).data
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return response.Response(
                data={
                    'status_code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Failed to get contributions',
                    'error': 'Failed to get contributions'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        

class GetReceiptView(RetrieveAPIView):
    serializer_class = (IsStrictlyAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        try:
            contribution = Contribution.objects.get(id=kwargs.get('contribution_id'))
            for payment in contribution.payments.all():
                if payment.user == request.user:
                    # send email notification
                    NotificationService.send_email(f'Payment Receipt!!!', f'Hello {request.user.name},\n\n' \
                        f'Kindly find attached below a copy of your payment receipt.\nAmount: ₦{contribution.amount}', request.user.email)
        except:
            pass

        return response.Response(
                data={
                    'status_code': status.HTTP_200_OK,
                    'message': 'Receipt sent to your email',
                },
                status=status.HTTP_200_OK
            )

