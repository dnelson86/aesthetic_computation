from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from PIL import Image

from aesthetic_computation.models import Post, Category

# custom error handlers
def handler404(request, *args, **argv):
    return render(request, 'ac/404.html', {})

def handler500(request, *args, **argv):
    return render(request, 'ac/500.html', {})

# home page (and category listing page)
def home(request, category_name=None):
    # get posts
    posts = Post.objects.all()

    # filter to only posts in a specified category
    if category_name is not None:
        try:
            cat = Category.objects.get(name=category_name)
            posts = cat.post_set.all()
        except:
            # category does not exist, redirect to home
            return HttpResponseRedirect(reverse('home'))

    context = {'posts':posts[::-1]}
    return render(request, 'ac/index.html', context)

# single post page
def post(request, id):
    # get post
    try:
        post = Post.objects.get(id=id)
        cats = post.categories.all()
    except:
        # post does not exist, redirect to home
        return HttpResponseRedirect(reverse('home'))

    # get previous and next posts for arrow links
    try:
        prev_post_id = Post.objects.get(id=int(id)-1).id
    except:
        prev_post_id = None

    try:
        next_post_id = Post.objects.get(id=int(id)+1).id
    except:
        next_post_id = None

    # check if image is sufficiently large that we can allow a big view
    wide_entry = ''

    try:
        with Image.open(post.image_large) as img:
            width, height = img.size
        if width >= 1400:
            wide_entry = ' wide-entry'
        if width >= 1700:
            wide_entry += ' wide-entry-xl'
    except:
        pass

    # render
    context = {'post':post, 'cats':cats, 'wide_entry':wide_entry,
               'prev_post_id':prev_post_id, 'next_post_id':next_post_id}
    return render(request, 'ac/post.html', context)
