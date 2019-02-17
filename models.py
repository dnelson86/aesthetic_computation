from django.db import models
from django.contrib import admin

import os.path

class Category(models.Model):
    """ Category, which can contain many Posts (and a Post can belong to one or more categories). """
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name

def upload_path_460px(instance, filename):
    fn, ext = os.path.splitext(filename)
    return "%d_460px%s" % (instance.id, ext)

def upload_path_large(instance, filename):
    fn, ext = os.path.splitext(filename)
    return "%d_large%s" % (instance.id, ext)

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

    image_460px = models.ImageField(upload_to=upload_path_460px)
    image_large = models.ImageField(upload_to=upload_path_large)

    categories  = models.ManyToManyField(Category)

    @property
    def categories_string(self):
        category_names = [cat.name for cat in self.categories.all()]
        return ", ".join(category_names)    

    def __str__(self):
        return self.title

    # save images with filenames based on model id
    def save(self, *args, **kwargs):
        if self.pk is None:
            # stash and erase (pk does not exist until super().save)
            saved_image1 = self.image_460px
            saved_image2 = self.image_large
            self.image_460px = None
            self.image_large = None

            # save and restore
            super(Post, self).save(*args, **kwargs)
            self.image_460px = saved_image1
            self.image_large = saved_image2

        # save restored
        super(Post, self).save(*args, **kwargs)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
