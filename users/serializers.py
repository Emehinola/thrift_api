from .models import User, Notification

from rest_framework.serializers import Serializer, ModelSerializer, CharField, FloatField, SerializerMethodField

class LoginSerializer(Serializer):
    email = CharField()
    password = CharField()


class UserSerializer(ModelSerializer):
    contribution_amount = FloatField()
    class Meta:
        model = User
        fields = ('email', 'name', 'phone', 'password', 'contribution_amount')

    def create(self, validated_data):
        password = validated_data.get('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        return user
    
class ListUserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'is_admin')

  

class RetrieveUserSerializer(ModelSerializer):    
    group = SerializerMethodField()

    class Meta:
        model = User
        exclude = ('password', 'is_admin')

    def get_group(self, obj):
        try:
            return obj.group.group.id
        except:
            pass
        return None

class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'