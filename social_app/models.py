from django.db import models
from django.contrib.auth.models import AbstractUser

class SocialUSer(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=250,unique=True,null=True,blank=True)
    def save(self,*args,**kwargs):
        self.username = self.email
        super(SocialUSer,self).save(*args,**kwargs)

    def __str__(self) -> str:
        return self.email


from django.contrib.auth import get_user_model

User = get_user_model()

class FriendRequest(models.Model):
  STATUS_CHOICES = [('pending', 'Pending'),('accepted', 'accepted'), ('rejected', 'rejected')]
  
  sender = models.ForeignKey(SocialUSer, related_name='sent_requests', on_delete=models.CASCADE)
  receiver = models.ForeignKey(SocialUSer, related_name='received_requests', on_delete=models.CASCADE)
  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self) -> str:
    return str(self.sender)+' To '+str(self.receiver)
    