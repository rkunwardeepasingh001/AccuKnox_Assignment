from django.db import models
from django.contrib.auth.models import AbstractUser

class SocialUSer(AbstractUser):
  email = models.EmailField(unique=True)
  username = models.CharField(max_length=250,
                              unique=True,
                              null=True,blank=True)
  name = models.CharField(max_length=100,
                          null=True,blank=True)
  def save(self,*args,**kwargs):
    self.username = self.email.lower()
    super(SocialUSer,self).save(*args,**kwargs)

  def __str__(self) -> str:
    return str(self.id)+" email= "+str(self.email)
  


class FriendRequest(models.Model):
  STATUS_CHOICES = [
                    ('pending', 'pending'),
                    ('accepted', 'accepted'),
                    ('rejected', 'rejected')
                  ]
  sender = models.ForeignKey(SocialUSer, 
                             related_name='sent_requests',
                             on_delete=models.CASCADE,
                             null=True,blank=True
                             )
  receiver = models.ForeignKey(SocialUSer,
                               related_name='received_requests',
                               on_delete=models.CASCADE,
                               null=True,blank=True)
  status = models.CharField(max_length=20,
                            choices=STATUS_CHOICES,
                            default='pending')
  created_at = models.DateTimeField(auto_now_add=True)

  # def __str__(self) -> str:
  #   return str(self.sender)+' To '+str(self.receiver)
  

class  Friend_List(models.Model):
  STATUS_CHOICES = [
                    ('pending', 'pending'),
                    ('accepted', 'accepted'),
                    ('rejected', 'rejected')
                  ]
  sender = models.ForeignKey(SocialUSer, 
                             related_name='sent',
                             on_delete=models.CASCADE,
                             null=True,blank=True
                             )
  receiver = models.ForeignKey(SocialUSer,
                               related_name='received',
                               on_delete=models.CASCADE,
                               null=True,blank=True)
  status = models.CharField(max_length=20,
                            choices=STATUS_CHOICES,
                            default='pending')
  created_at = models.DateTimeField(auto_now_add=True)



# class CustomUser(models.Model):
#   phone_number = models.CharField(max_length=50)  
#   gender = models.CharField(max_length=50)