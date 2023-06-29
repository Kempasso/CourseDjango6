from django.conf import settings
from django.db import models
from django.db.models import CASCADE

from users.models import User


class Ad(models.Model):
    image = models.ImageField(upload_to='django_media', null=True, blank=True)
    title = models.CharField(max_length=50)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=CASCADE)


class Comment(models.Model):
    text = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=CASCADE)
    ad = models.ForeignKey(Ad, on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now=True)



