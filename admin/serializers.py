from rest_framework.serializers import Serializer, IntegerField, BooleanField


class DisburseFundSerializer(Serializer):
    contribution_id = IntegerField()
