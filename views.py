from django.shortcuts import render
#from django.http import HttpResponse, HttpResponseRedirect
#from django.core.exceptions import PermissionDenied
#from django.core.urlresolvers import reverse

from aesthetic_computation.models import Post

# custom error handlers
def handler404(request, *args, **argv):
    return render(request, 'ac/404.html', {})

def handler500(request, *args, **argv):
    return render(request, 'ac/500.html', {})

# home page (and category listing page)
def home(request, category=None):
    if category is not None:
        # filter
        pass

    # get posts
    posts = [{'id':1, 'title':'test here'},
             {'id':1, 'title':'test here2'},
             {'id':1, 'title':'test here3'},
             {'id':1, 'title':'test here4'},
             {'id':1, 'title':'test here5'},
             {'id':1, 'title':'test here6'},
             {'id':1, 'title':'test here7'},
             {'id':1, 'title':'test here3'},
             {'id':1, 'title':'test here4'},
             {'id':1, 'title':'test here5'},
             {'id':1, 'title':'test here6'},
             {'id':1, 'title':'test here7'},
             {'id':1, 'title':'test here3'},
             {'id':1, 'title':'test here4'},
             {'id':1, 'title':'test here5'},
             {'id':1, 'title':'test here6'},
             {'id':1, 'title':'test here7'},]

    context = {'posts':posts}
    return render(request, 'ac/index.html', context)

# single post page
def post(request, id):
    # get post
    post = {'id':1, 'title':'Auriga 13b'}

    context = {'post':post}
    return render(request, 'ac/post.html', context)
