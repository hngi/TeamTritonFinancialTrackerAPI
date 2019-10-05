from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Expense(models.Model):
    created_by = models.CharField(max_length=255, editable=False)
    created_on = models.CharField(max_length=255, editable=False)
    purchase_date = models.DateField(blank=True)  #I was thinking we should add a date and time for tracking
    item = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    amount = models.IntegerField()

    class Meta:
        db_table = 'expense'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=11, blank=True)
    limit = models.IntegerField(blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()