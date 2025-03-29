from rest_framework.serializers import ModelSerializer, IntegerField, SerializerMethodField, CharField, Serializer, FloatField
from .models import Group, UserGroup, Contribution, PaymentStatus, ContributionStatus, ContributionPayment, PayoutStatus
from users.serializers import WalletSerializer
from users.models import Wallet


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class UserGroupSerializer(ModelSerializer):
    class Meta:
        model = UserGroup
        fields = '__all__'


class ContributionSerializer(ModelSerializer):
    class Meta:
        model = Contribution
        fields = '__all__'


class DashboardGroupSerializer(ModelSerializer):
    members_count = SerializerMethodField()
    last_paid_obj = SerializerMethodField()

    class Meta:
        model = Group
        fields = '__all__'

    def get_members_count(self, obj):
        return obj.users.count()
    
    def get_last_paid_obj(self, obj):
        last_obj = {
            'name': None,
            'date': None,
            'position': None
        }
        try:
            for contribution in obj.contributions.all():
                if contribution.status == ContributionStatus.ACTIVE:
                    payment = contribution.payments.last()
                    last_obj['name'] = payment.user.name
                    last_obj['date'] = payment.date_paid
                    last_obj['position'] = contribution.position
                    return last_obj
        except Exception as e:
            return None

class AdminContributionSerializer(ModelSerializer):
    class Meta:
        model = Contribution
        fields = '__all__'

class SelfContributionSerializer(ModelSerializer):
    my_payment_status = SerializerMethodField()
    payment_date = SerializerMethodField()

    class Meta:
        model = Contribution
        fields = '__all__'

    def get_my_payment_status(self, obj):
        try:
            for payment in obj.payments.all():
                if payment.user == self.context['user']:
                    return payment.status
        except:
            pass
        return PaymentStatus.UPCOMING
    
    
    def get_payment_date(self, obj):
        try:
            for payment in obj.payments.all():
                if payment.user == self.context['user']:
                    return payment.date_paid
        except:
            pass
        return None

    

class UserDashboardSerializer(Serializer):
    amount_contributed = SerializerMethodField()
    total_contributed = SerializerMethodField()
    group = SerializerMethodField()
    countdown = SerializerMethodField()
    member_contribution_status = SerializerMethodField()
    upcoming_payouts = SerializerMethodField()
    my_rotation = SerializerMethodField()
    contribution = SerializerMethodField()
    is_my_turn = SerializerMethodField()
    wallet = SerializerMethodField()


    def get_amount_contributed(self, obj):
        user = self.context['user']
        amount = 0
        try:
            for payment in user.payments.all():
                amount += payment.amount
        except:
            pass
        return amount
    
    def get_total_contributed(self, obj):
        user = self.context['user']
        amount = 0
        try:
            for payment in user.payments.all():
                amount += payment.amount
        except:
            pass
        return amount
    
    def get_group(self, obj):
        user = self.context['user']
        try:
            return {
                'id': user.groups.last().id,
                'name': user.groups.last().name,
                'description': user.groups.last().description,
                'status': user.groups.last().status
            }
        except:
            return None
    
    def get_countdown(self, obj):
        return 5
    
    def get_member_contribution_status(self, obj):
        return '10/12'
    
    def get_upcoming_payouts(self, obj):
        try:
            user = self.context['user']
            contributions = user.groups.last().contributions.all()
            return [
                {
                    'position': i.position,
                    'name': i.payout_to.name if i.payout_to != None else None,
                    'amount': i.amount,
                    'date': i.end_date
                }

                for i in contributions if i.payout_status == PayoutStatus.UPCOMING
            ]
        except Exception as e:
            pass
        return []
    
    def get_my_rotation(self, obj):
        try:
            user = self.context['user']
            contributions = user.groups.last().contributions.all()
            
            for contr in contributions:
                if contr.payout_to == user:
                    return {
                        'position': contr.position,
                        'name': contr.payout_to.name if contr.payout_to != None else None,
                        'amount': contr.amount,
                        'status': contr.payout_status,
                        'date': contr.end_date
                    }
        except Exception as e:
            pass
        return None
    

    def get_contribution(self, obj):
        try:
            user = self.context['user']
            for contri in user.group.group.contributions.all():
                if contri.status == ContributionStatus.ACTIVE:
                    return ContributionSerializer(contri).data
        except: 

            pass

    
    def get_is_my_turn(self, obj):
        try:
            user = self.context['user']
            for contri in user.group.contributions.all():
                if (contri.status == ContributionStatus.ACTIVE) & contri.payout_to == user:
                    return True
        except: pass
        return False
    
    def get_wallet(self, obj):
        try:
            wallet, created = Wallet.objects.get_or_create(user=self.context['user'])
            return WalletSerializer(wallet).data
        except Exception as e:
            print(e)
            pass
        return None


    