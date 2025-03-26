from rest_framework.serializers import ModelSerializer, IntegerField, SerializerMethodField, CharField
from .models import Group, UserGroup, Contribution, PaymentStatus, ContributionStatus

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