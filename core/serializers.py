from rest_framework import serializers
from .models import *
import string
import random

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'fullname', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
def generate_short_url():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=6))

class URLCreateSerializer(serializers.ModelSerializer):
    short_url = serializers.CharField(required=False)

    class Meta:
        model = URL
        fields = ['original_url', 'short_url']
    
    def validate_short_url(self, value):
        if URL.objects.filter(short_url=value).exists():
            raise serializers.ValidationError("This short URL is already taken.")
        return value
    
    def create(self, validated_data):
        request = self.context['request']
        user = request.user

        if 'short_url' not in validated_data or not validated_data['short_url']:
            while True:
                short = generate_short_url()
                if not URL.objects.filter(short_url=short).exists():
                    validated_data['short_url'] = short
                    break

        validated_data['created_by'] = user
        return super().create(validated_data)