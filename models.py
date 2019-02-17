from django.db import models
from django.conf import settings
from datetime import datetime

class Post(models.Model):
    """ Single post. """
    title       = models.CharField(max_length=200)
    author      = models.TextField()
    origin_text = models.TextField()
    origin_link = models.URLField()

    description = models.TextField()
    methods     = models.TextField()
    date_added  = models.DateField(auto_now_add=True)

    # todo: categories
