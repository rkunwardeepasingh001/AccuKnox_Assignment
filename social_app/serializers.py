from rest_framework import serializers
from .models import SocialUSer, FriendRequest
class SocialUSerSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True)
  class Meta:
    model = SocialUSer
    fields = ['username','email','password']

class LoginSerializer(serializers.ModelSerializer):
  class Meta:
    model = SocialUSer
    fields = ['email','password']


class FriendRequestSerializer(serializers.ModelSerializer):
  class Meta:
    model = FriendRequest
    fields ="__all__"

  def create(self, validated_data):
    return FriendRequest.objects.create(**validated_data)
