from rest_framework.serializers import Serializer, CharField, FloatField, IntegerField, BooleanField


class FundContributionSerializer(Serializer):
    amount  = FloatField()
    contribution_id = IntegerField()
    is_wallet = BooleanField()
