from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view, permission_classes,APIView
from .serializers import SocialUSerSerializer, LoginSerializer
from rest_framework.response import Response
from django.contrib.auth import authenticate,login
from rest_framework import status

from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
def Sign_up(request):
  data=request.data
  ser = SocialUSerSerializer(data=data)
  if ser.is_valid():
    new_ser = ser.save()
    new_ser.set_password(data['password'])
    new_ser.save()
    return Response(("Successfully Created Data !",ser.data))
  return Response("Already Signup these User  !")

@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
      
        if not email or not password:
            return Response({"error": "Both email and password are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(request, username=email, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return Response({'success': "Login successful"}, status=status.HTTP_200_OK)
    return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


User = get_user_model()
class UserSearchAPIView(generics.ListAPIView):
    serializer_class = LoginSerializer
    pagination_class = PageNumberPagination
    page_size = 10
    permission_classes = [IsAuthenticated]
    
    def get(self,request,pk=None):
      name = self.request.query_params.get('email', None)
      if name is not None:
        queryset = User.objects.filter(email__istartswith=name)
        serilaizer = SocialUSerSerializer(queryset,many=True)
        return Response(serilaizer.data,status=status.HTTP_200_OK )
      return Response("Not Found !")


from .models import FriendRequest
from .serializers import FriendRequestSerializer
from django.core.cache import cache

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_friend_request(request):
    sender_email = request.data.get('sender_email')
    receiver_email = request.data.get('receiver_email')
    if sender_email ==  receiver_email:
      return Response({"error": "You cannot send a friend request to yourself."},status=status.HTTP_400_BAD_REQUEST)
    
    if not sender_email or not receiver_email:
        return Response("Sender email and receiver email are required.", status=status.HTTP_400_BAD_REQUEST)
    
    sender = get_user_model().objects.filter(email=sender_email).first()
    receiver = get_user_model().objects.filter(email=receiver_email).first()
    
    if not sender or not receiver:
      return Response("Sender or receiver not found.", status=status.HTTP_404_NOT_FOUND)
    
    if FriendRequest.objects.filter(sender=sender, receiver=receiver).exists():
      return Response("Friend request already sent.", status=status.HTTP_400_BAD_REQUEST)
    
    rate_limit_key = f"friend_request_limit_{sender_email}"
    request_count = cache.get(rate_limit_key, 0)
    if request_count >= 3:
      return Response("You have reached the limit of friend requests within a minute.", status=status.HTTP_429_TOO_MANY_REQUESTS)

    cache.set(rate_limit_key, request_count + 1, timeout=60)
    
    
    serializer = FriendRequestSerializer(data={'sender': sender.id, 'receiver': receiver.id})
    if serializer.is_valid():
      serializer.save()
      return Response("Friend request sent successfully.", status=status.HTTP_201_CREATED)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

 

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def accept_friend_request(request, id):
  friend_request = get_object_or_404(FriendRequest,id=id)
  ser = FriendRequestSerializer(friend_request,data=request.data,partial=True)
  if ser.is_valid():
    ser.save()
    return Response("Friend request accepted successfully.", status=status.HTTP_200_OK)
  return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def reject_friend_request(request, id):
  friend_request = get_object_or_404(FriendRequest,id=id)
  friend_request.delete()
  return Response("Deleted Friend Request !")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def List(request):
  querryset = FriendRequest.objects.filter(status__iexact="accepted")
  serializer = FriendRequestSerializer(querryset,many=True)
  return Response(serializer.data)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ListPending(request):
  querryset = FriendRequest.objects.filter(status__iexact="Pending")
  serializer = FriendRequestSerializer(querryset,many=True)
  return Response(serializer.data)

