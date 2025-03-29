from rest_framework.serializers import Serializer, IntegerField, BooleanField, FloatField, CharField


class DisburseFundSerializer(Serializer):
    contribution_id = IntegerField()

class PayoutScheduleSerializer(Serializer):
    next_recipient = CharField()
    amount = FloatField()
    date = CharField()


class AdminDashboardSerializer(Serializer):
    current_members = IntegerField()
    new_members = IntegerField()
    current_groups = IntegerField()
    active_groups = IntegerField()
    total_contribution = FloatField()
    total_payouts = FloatField()
    members_contributed = IntegerField()
    members_contribution_pending = IntegerField()
