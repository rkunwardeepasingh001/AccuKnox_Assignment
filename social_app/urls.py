from django.urls import path
from .views import  login_view, Sign_up, UserSearchAPIView, send_friend_request, accept_friend_request,reject_friend_request,List,ListPending


urlpatterns = [
  path("login/",login_view,name = "Log_in"),
  path("Sign_up/",Sign_up, name = "Sign_up"),
  path("search_users/",UserSearchAPIView.as_view(), name = "search_users"),
  path("send_friend_request/",send_friend_request, name="send_friend_request"),
  path("accept_friend_request/<int:id>/",accept_friend_request, name="accept_friend_request"),
  path("reject_friend_request/<int:id>/",reject_friend_request, name="reject_friend_request"),
  path("list/",List,name="list"),
  path("ListPending/",ListPending,name="ListPending"),
]