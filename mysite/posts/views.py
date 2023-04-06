from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from django.views import View
from itertools import chain
from .models import *


class PostIndexView(View):
    def get(self, request):
        """Returns HttpResponse containing index page listing all posts in order of posting

        Returns:
            HttpResponse: index.html with context: posts
        """
        # This doesnt work when theres no post objects in the db
        posts = list(chain(BlogPost.objects.filter(),
                     AlbumPost.objects.filter(), VideoPost.objects.filter()))
        context = {'posts': posts}
        return render(request, 'posts/index.html', context)


class DetailView(View):
    def get(self, request, pk):
        """Returns HttpResponse containing detail page listing:
        The relevant post's attributes
        The relevant post's comments

        Returns:
            HttpResponse: relevent post_detail.html with context: post, comments
        """
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        if post.get_post_type() == 'Blog':
            context = {
                'blogpost': post,
                'comments': post.comments.order_by('-posted_date')
            }
            return render(request, 'posts/blog_post_detail.html', context)
        elif post.get_post_type() == 'Album':
            context = {
                'albumpost': post,
                'comments': post.comments.order_by('-posted_date')
            }
            return render(request, 'posts/album_post_detail.html', context)
        elif post.get_post_type() == 'Video':
            context = {
                'videopost': post,
                'comments': post.comments.order_by('-posted_date')
            }
            return render(request, 'posts/video_post_detail.html', context)
        else:
            return HttpResponseNotFound('<h1>Page not found: invalid post type</h1>')


class UserDetailView(View):
    def get(self, request, pk):
        """Returns HttpResponse containing personal account page listing:
        The specified user's details

        Returns:
            HttpResponse: user_detail.html with context: user
        """
        context = {
            'user': get_object_or_404(CustomUser, pk=self.kwargs['pk']),
        }
        return render(request, 'posts/user_detail.html', context)


class MyAccountView(View):
    def get(self, request):
        """Returns HttpResponse containing the logged in user's personal account page listing:
        The user's details

        Returns:
            HttpResponse: my_account.html with context: user
        """
        # Fix this once authentication is implemented
        logged_in_user = 1
        context = {
            'user': get_object_or_404(CustomUser, pk=logged_in_user),
        }
        return render(request, 'posts/my_account.html', context)


class LoginView(View):
    def get(self, request):
        """Returns HttpResponse containing login page

        Returns:
            HttpResponse: login.html
        """
        return render(request, 'posts/login.html')
