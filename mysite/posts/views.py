from django.http import HttpResponseRedirect
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


class BlogPostDetailView(View):    
    def get(self, request, pk):
        """Returns HttpResponse containing detail page listing:
        The relevant blog post's details
        The relevant blog post's comments

        Returns:
            HttpResponse: blog_post_detail.html with context: post, comments
        """
        context = {
            'blogpost' : get_object_or_404(BlogPost, pk=self.kwargs['pk']),
            'comments' : get_object_or_404(BlogPost, pk=self.kwargs['pk']).comments.order_by('-posted_date')
        }
        return render(request, 'posts/blog_post_detail.html', context)


class AlbumPostDetailView(View):    
    def get(self, request, pk):
        """Returns HttpResponse containing detail page listing:
        The relevant album post's details
        The relevant album post's comments

        Returns:
            HttpResponse: album_post_detail.html with context: post, comments
        """
        context = {
            'albumpost' : get_object_or_404(AlbumPost, pk=self.kwargs['pk']),
            'comments' : get_object_or_404(AlbumPost, pk=self.kwargs['pk']).comments.order_by('-posted_date')
        }
        return render(request, 'posts/album_post_detail.html', context)


class VideoPostDetailView(View):    
    def get(self, request, pk):
        """Returns HttpResponse containing detail page listing:
        The relevant video post's details
        The relevant video post's comments

        Returns:
            HttpResponse: video_post_detail.html with context: post, comments
        """
        context = {
            'videopost' : get_object_or_404(VideoPost, pk=self.kwargs['pk']),
            'comments' : get_object_or_404(VideoPost, pk=self.kwargs['pk']).comments.order_by('-posted_date'),
        }
        return render(request, 'posts/video_post_detail.html', context)


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

