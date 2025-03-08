from .models import User

from rest_framework.serializers import Serializer, ModelSerializer, CharField

class LoginSerializer(Serializer):
    email = CharField()
    password = CharField()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'name', 'phone', 'password')

    def create(self, validated_data):
        password = validated_data.get('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        return user
    

class RetrieveUserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'is_admin')

