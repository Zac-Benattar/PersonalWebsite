from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.urls import reverse
from django.views import View
from django.utils import timezone
from itertools import chain

from .models import *

# from static.Risk_Assessment.projectevaluator import ProjectEvaluator

class PostIndexView(View):
    def get(self, request):
        """Returns HttpResponse containing index page listing all posts in order of posting

        Returns:
            HttpResponse: index.html with context: posts
        """
        # This doesnt work when theres no post objects in the db
        posts = list(chain(BlogPost.objects.filter(), AlbumPost.objects.filter(), VideoPost.objects.filter()))
        context = {'posts':posts}
        return render(request, 'posts/index.html', context)


class DetailView(View):    
    def get(self, request, pk):
        """Returns HttpResponse containing detail page listing:
        The relevant post's attributes
        The relevant post's comments

        Returns:
            HttpResponse: relevent post_detail.html page with context: post, comments
        """
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        if post.get_post_type() == 'Blog':
            context = {
                'blogpost' : post,
                'comments' : post.comments.order_by('-posted_date')
            }
            return render(request, 'posts/blog_post_detail.html', context)
        elif post.get_post_type() == 'Album':
            context = {
                'albumpost' : post,
                'comments' : post.comments.order_by('-posted_date')
            }
            return render(request, 'posts/album_post_detail.html', context)
        elif post.get_post_type() == 'Video':
            context = {
                'videopost' : post,
                'comments' : post.comments.order_by('-posted_date')
            }
            return render(request, 'posts/video_post_detail.html', context)
        else:
            return HttpResponseNotFound('<h1>Page not found: invalid post type</h1>')


class AccountView(View):
    def get(self, request, pk):
        """Returns HttpResponse containing personal account page listing:
        The user's details

        Returns:
            HttpResponse: people.html with context: user
        """
        context = {
            'user' : get_object_or_404(CustomUser, pk=self.kwargs['pk']),
        }
        return render(request, 'posts/myaccount.html', context)


class LoginView(View):
    def get(self, request):
        """Returns HttpResponse containing login page

        Returns:
            HttpResponse: login.html
        """
        return render(request, 'posts/login.html')
