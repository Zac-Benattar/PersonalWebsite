from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.urls import reverse
from django.views import View
from django.utils import timezone

from .models import *

# from static.Risk_Assessment.projectevaluator import ProjectEvaluator

class IndexView(View):
    def get(self, request):
        """Returns HttpResponse containing index page listing all posts in order of posting

        Returns:
            HttpResponse: index.html with context: posts
        """
        # This doesnt work when theres no post objects in the db
        posts = Post.objects.all()
        if posts.count > 0:
            posts = posts.order_by('-posted_date')
        context = {'posts':posts}
        return render(request, 'posts/index.html', context)


class DetailView(View):    
    def get(self, request, pk):
        """Returns HttpResponse containing detail page listing:
        The relevant post's details
        The relevant post's comments

        Returns:
            HttpResponse: detail.html with context: post, comments
        """
        context = {
            'post' : get_object_or_404(Post, pk=self.kwargs['pk']),
            'comments' : Comment.objects.filter(post=get_object_or_404(Post, pk=self.kwargs['pk'])).order_by('-posted_date').last()
        }
        return render(request, 'posts/detail.html', context)


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

