from rest_framework.serializers import Serializer, IntegerField


class DisburseFundSerializer(Serializer):
    contribution_id = IntegerField()