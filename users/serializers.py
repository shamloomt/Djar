from rest_framework import serializers
from users.models import UserAccount, Trust
from django.contrib.auth.hashers import make_password

class Users_Serializer(serializers.ModelSerializer):

    class Meta:
        model = UserAccount
        fields = '__all__'

    def create(self, validated_data):

        user = UserAccount(
            username=validated_data['username'],
            password = make_password(validated_data['password']),
            is_active = True
        )

        user.save()
        return user

# class CreateUserSerializer(serializers.ModelSerializer):
#   class Meta:

#     model = UserAccount
#     fields = ('username', 'password', 'is_active')

class Trust_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Trust
        fields = '__all__'


    