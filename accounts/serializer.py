from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['full_name'] = user.first_name + user.last_name
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        username = attrs.get(self.username_field)
        password = attrs.get("password")
        
        user = authenticate(request=self.context.get('request'), username=username, password=password)
        if user:
            if user.is_superuser:
                refresh = self.get_token(user)
                data['refresh'] = str(refresh)
                data['access'] = str(refresh.access_token)
            else:
                raise serializers.ValidationError("User is not a superuser.")
        else:
            raise serializers.ValidationError("Unable to log in with provided credentials.")
        
        return data
