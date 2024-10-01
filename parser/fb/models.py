from django.db import models

class FbGroup(models.Model):
    group_id = models.CharField(max_length=20, default=None, null=True)
    likes_count = models.PositiveIntegerField(default=None, null=True)
    followers_count = models.PositiveIntegerField(default=None, null=True)
    url = models.CharField(max_length=255, unique=True)
    is_used = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    ads_count = models.PositiveIntegerField(default=None, null=True)