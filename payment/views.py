from rest_framework.generics import CreateAPIView
from rest_framework import response, status

from .serializers import FundContributionSerializer
from contribution.models import Contribution, ContributionPayment, PaymentStatus
from core.permissions import IsAuthenticated

from services.notification_service import NotificationService

class FundContributionView(CreateAPIView):
    serializer_class = FundContributionSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = FundContributionSerializer(data=request.data)
        contribution = None
        if serializer.is_valid():
            if not serializer.validated_data.get('is_wallet'):
                contribution = Contribution.objects.filter(id=serializer.validated_data.get('contribution_id')).first()
                if contribution is None:
                    return response.Response(
                        status=status.HTTP_404_NOT_FOUND,
                        data={
                            'status_code': status.HTTP_404_NOT_FOUND,
                            'message': 'Contribution not found',
                            'error': 'Contribution not found'
                        },
                    ) # contribution object does not exist
            
                if serializer.validated_data.get('amount') != contribution.amount:
                    return response.Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data={
                            'status_code': status.HTTP_400_BAD_REQUEST,
                            'message': 'Contribution amount mismatch',
                            'error': 'Contribution amount mismatch'
                        },
                    ) # amount not equal to the expected contribution amount
            
            if serializer.validated_data.get('is_wallet'):
                request.user.wallet.amount += serializer.validated_data.get('amount')
                request.user.wallet.save()
                try:
                    # send email notification
                    NotificationService.send_email(f'Wallet Funded!!!', f'Hello {request.user.name},\n\n' f"You have successfully funded your wallet\nAmount: ₦{serializer.validated_data.get('amount')}", request.user.email)
                except:
                    pass
            else:
                contribution_payment = ContributionPayment(
                        contribution=contribution,
                        amount=serializer.validated_data.get('amount'),
                        status=PaymentStatus.PAID,
                        user=request.user, # currently logged in user
                        payment_method='card'
                    )
                contribution_payment.save()
                try:
                    # send email notification
                    NotificationService.send_email(f'Contribution Funded!!!', f'Hello {request.user.name},\n\n' \
                            f'You have successfully funded your contribution for this month\nAmount: ₦{contribution.amount}', request.user.email)
                except:
                    pass

            return response.Response(
                    status=status.HTTP_200_OK,
                    data={
                        'status_code': status.HTTP_200_OK,
                        'message': 'Contribution successful',
                        'data': serializer.data
                    },
                )
        return response.Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    'status_code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Contribution failed',
                    'data': serializer.errors
                },
            )
        
    