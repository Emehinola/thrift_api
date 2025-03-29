from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from rest_framework.authtoken.models import Token

from users.serializers import UserSerializer, LoginSerializer, RetrieveUserSerializer
from users.models import User, NotificationType, Notification
from contribution.models import Contribution, ContributionStatus, PayoutStatus, Group
from core.permissions import IsAuthenticated, IsAdmin

from services.notification_service import NotificationService



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
            group = Group.objects.get('group_id')
            
            if group.users.count() >= 12:
                return Response(
                    status=HTTP_400_BAD_REQUEST,
                    data={
                        'status_code': HTTP_400_BAD_REQUEST,
                        'message': 'User addition to group failed',
                        'data': 'Group already have up to 12 members'
                    },
                )
            
            user.groups.add(kwargs.get('group_id')) # add user to group
            print("here")
            try:
                NotificationService.send_email(f'Group Notification', 'Hello {user.name},\n\n' \
                'You have been added to a thrift contribution group.\nGroup name: ${group.name}\nYour turn: {user.group.position}', user.email)
            except:
                pass

            for contribution in group.contributions:
                if contribution.postition == user.group.postition:
                    contribution.set_payout_to(user) # set user rotation

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
    

class DisburseFundView(CreateAPIView):
    permission_classes = (IsAuthenticated, IsAdmin)

    def post(self, request, *args, **kwargs):
        try:
            contribution = Contribution.objects.get(id=kwargs.get('contribution_id'))
            if contribution.can_disburse[0]:
                contribution.status = ContributionStatus.COMPLETED
                contribution.payout_status = PayoutStatus.RECEIVED
                contribution.save()

                try:
                    # send email notification
                    NotificationService.send_email(f'Payment Disbursement', 'Hello {user.name},\n\n' \
                    f'You have been paid an amount of ₦{contribution.expected_amount}.\nGroup name: {contribution.group.name}\nYour turn: {contribution.payout_to.group.position}', contribution.payout_to.email)
                except:
                    pass

                # create notification
                Notification.objects.create(
                    user=contribution.payout_to,
                    notification_type=NotificationType.CONTRIBUTION_DISBURSEMENT,
                    message=f'You have received a payout of ₦{contribution.amount} from {contribution.group.name}',
                    amount=contribution.expected_amount
                )

                return Response(
                    status=HTTP_200_OK,
                    data={
                        'status_code': HTTP_200_OK,
                        'message': 'Fund disbursed successfully',
                        'data': None
                    },
                )
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={
                    'status_code': HTTP_400_BAD_REQUEST,
                    'message': 'Disbursement failed',
                    'error': contribution.can_disburse[1]
                },
            )
            
        except Contribution.DoesNotExist:
            return Response(
                status=HTTP_404_NOT_FOUND,
                data={
                    'status_code': HTTP_404_NOT_FOUND,
                    'message': 'Contribution not found',
                    'error': 'Contribution not found'
                },
            )