from rest_framework.serializers import Serializer, CharField, FloatField, IntegerField


class FundContributionSerializer(Serializer):
    amount  = FloatField()
    contribution_id = IntegerField()
