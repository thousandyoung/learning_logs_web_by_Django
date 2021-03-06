from django.db import models
from django.contrib.auth.models import User
from mdeditor.fields import MDTextField
from taggit.managers import TaggableManager


# Create your models here.
class Topic(models.Model):
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, )
    entry_num = models.IntegerField(default=0)

    def __str__(self):
        return self.text


class Entry(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, )
    title = models.CharField(max_length=200, default="let's start !")
    body = models.TextField(default="The entry is empty")
    text = MDTextField()
    date_added = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager(blank=True)

    class Meta:
        verbose_name_plural = 'Entries'

    def __str__(self):
        return self.text[:50] + '...'
