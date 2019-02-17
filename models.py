from django.db import models
#from django.conf import settings
from django.contrib import admin
#from datetime import datetime

class Category(models.Model):
    """ Category, which can contain many Posts (and a Post can belong to one or more categories). """
    name = models.CharField(max_length=60)
    # post_set

    def __str__(self):
        return self.name

class Post(models.Model):
    """ Single post. """
    title       = models.CharField(max_length=200)
    author      = models.TextField()
    author_link = models.URLField(blank=True)
    origin_text = models.TextField()
    origin_link = models.URLField(blank=True)

    description = models.TextField()
    methods     = models.TextField(blank=True)
    date_added  = models.DateField(auto_now_add=True)

    categories  = models.ManyToManyField(Category)

    @property
    def categories_string(self):
        category_names = [cat.name for cat in self.categories.all()]
        return ", ".join(category_names)    

    def __str__(self):
        return self.title

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
