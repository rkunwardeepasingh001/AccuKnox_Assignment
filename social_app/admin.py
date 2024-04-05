from django.contrib import admin
from .models import SocialUSer,FriendRequest,Friend_List#,CustomUser

admin.site.register(SocialUSer)
admin.site.register(FriendRequest)
admin.site.register(Friend_List)
# admin.site.register(CustomUser)
# Register your models here.
