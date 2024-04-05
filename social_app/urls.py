from django.urls import path
from .views import  FriendRequestOnMyAccount, UserSearchAPIView, SendFriendRequestAPIView, Accept_Friend_Request,ListAccepted,ListPending


urlpatterns = [
  # path("login/",login_view,name = "Log_in"),
  # path("Sign_up/",Sign_up, name = "Sign_up"),
  path("search_users/",UserSearchAPIView.as_view(), name = "search_users"),
  path("send_friend_request/",SendFriendRequestAPIView.as_view(), name="send_friend_request"),
  path("accept_friend_request/<int:id>/",Accept_Friend_Request.as_view(), name="accept_friend_request"),
  # path("accept_friend_request/",Accept_Friend_Request.as_view(), name="accept_friend_request"),#for testing
  path("listAccept/",ListAccepted.as_view(),name="listAccept"),
  path("ListPending/",ListPending.as_view(),name="ListPending"),
  path("request_my_account/",FriendRequestOnMyAccount.as_view(),name="requ est_my_account"),
  
]