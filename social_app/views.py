from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view, permission_classes,APIView
from .serializers import SocialUSerSerializer
from rest_framework.response import Response
from django.contrib.auth import authenticate,login
from rest_framework import status
from .models import *
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import FriendRequest
from .serializers import *
from django.db.models import Q
from rest_framework.throttling import UserRateThrottle

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def Sign_up(request):
#     if request.method == 'POST':
#       data = request.data
#       ser = SocialUSerSerializer(data=data)
#       if ser.is_valid():
#         new_ser = ser.save()
#         new_ser.set_password(data['password'])
#         new_ser.save()
#         return Response(("Successfully Created Data !",ser.data))
#       return Response(ser.errors)
#     return Response("Already Signup these User  !")

# @api_view(['POST'])
# @permission_classes([AllowAny]) 
# def login_view(request):
#     if request.method == 'POST':
#         email = request.data.get('email')
#         password = request.data.get('password')
      
#         if not email or not password:
#             return Response({"error": "Both email and password are required"}, status=status.HTTP_400_BAD_REQUEST)
        
#         user = authenticate(request, username=email, password=password)
#         print(user)
#         if user is not None:
#             login(request, user)
#             return Response({'success': "Login successful"}, status=status.HTTP_200_OK)
#     return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class UserSearchAPIView(generics.ListAPIView):
  serializer_class = SocialUSerSerializer
  pagination_class = PageNumberPagination
  queryset = SocialUSer.objects.all()
  filter_backends = [filters.SearchFilter]
  search_fields = ['=email','name__icontains']



class FriendRequestThrottle(UserRateThrottle):  
    # limit = '3/minute'                              
    scope = 'friend' 

class SendFriendRequestAPIView(APIView):
  permission_classes = [IsAuthenticated]
  throttle_classes = [FriendRequestThrottle]
 
  
  def post(self, request):
      receiver = request.data.get("receiver")
      serializer = FriendRequestSerializer(data=request.data)
      if serializer.is_valid():
          data = serializer.validated_data 
          req = FriendRequest(**data)
          req.sender = request.user
          if receiver == request.user.id:
              return Response("can not send friend request to yourself")
          if not (
               FriendRequest.objects.filter(
                  receiver=request.user.id, sender=receiver
              ).exists()):
              queryset = FriendRequest.objects.filter(
                  sender=request.user.id, receiver=receiver
              ).first()
              if not queryset:
                  req.save()
                  return Response(serializer.data, status=status.HTTP_201_CREATED)
              return Response("all ready exist")
          return Response(f"you have friend request from {receiver} ")
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    

class Accept_Friend_Request(APIView):

  def patch(self,request, id):
    status = request.data.get("status")
    friend_request = get_object_or_404(FriendRequest,id=id)
    ser = FriendRequestSerializer(friend_request, data=request.data, partial=True)
    if ser.is_valid():
      ser.save()
      if status == "accepted":
        qu = FriendRequest.objects.get(id=id)
        sender = qu.sender
        receiver = qu.receiver
        print(sender)
        print(receiver)
        qu2 = Friend_List.objects.create(sender=sender,receiver=request.user,status=status)
        qu.delete()
        return Response({"status":"Friend request accepted successfully."})
      elif status == "rejected":
        return Response("Friend request rejected successfully.", status=status.HTTP_200_OK)

    return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)

  

class ListAccepted(APIView):
  def get(self, request):
    queryset = Friend_List.objects.filter(Q(sender=request.user) | Q(receiver=request.user), status='accepted')
    serializer= FriendRequestSerializer(queryset, many=True)
    return Response(serializer.data)


class ListPending(APIView):
  def get(self, request):
    queryset = FriendRequest.objects.filter(receiver=request.user, status='pending')
    serializer= FriendRequestSerializer(queryset, many=True)
    return Response(serializer.data)



class FriendRequestOnMyAccount(APIView):
   def get(self, request):
      queryset = FriendRequest.objects.filter(receiver = request.user)
      serializer = FriendRequestSerializer(queryset, many=True)
      return Response(serializer.data)
       
