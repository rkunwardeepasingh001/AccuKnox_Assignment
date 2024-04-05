from rest_framework import serializers
from .models import *
class SocialUSerSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True)
  class Meta:
    model = SocialUSer
    fields = ['username','email','password','name']

# class LoginSerializer(serializers.ModelSerializer):
#   class Meta:
#     model = SocialUSer
#     fields = ['email','password']


class FriendRequestSerializer(serializers.ModelSerializer):
  class Meta:
    model = FriendRequest
    fields ="__all__"

class Friend_List_Serializer(serializers.ModelSerializer):
  class Meta:
    model = Friend_List
    fields = ['sender','receiver','status','created_at']