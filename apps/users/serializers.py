from rest_framework import serializers
from apps.users.models import User


class RegisterSerializers(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)
    
    class Meta:
        model = User
        fields = ["email", "password"]
    
    def validate_email(self, value):
        return value.lower()
    
    def validate(self, attrs):
        if attrs["password"] != attrs["confirm"]:
            raise serializers.ValidationError("Passwords don't match")
        return attrs