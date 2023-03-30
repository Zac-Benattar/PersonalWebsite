from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import permissions, viewsets
from projects.models import *
from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import NotFound
from rest_framework.decorators import permission_classes, action
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response

import sys #Import system file to add extra imports from outside file
import pathlib #Import the libary to modify paths

# Keeping in case need to add subfolder to path
# Add the Risk_Assessment folder to the path
# Search path needs to be changed to find the files, later reverted
# originalPath = sys.path
# folderpath = str(pathlib.Path(__file__).parent.parent.joinpath('static\Risk_Assessment').resolve())
# sys.path.append(folderpath)

# Revert the import path to the original path
# Might not be needed
# sys.path = originalPath

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# read permissions for authenticated users
class IsOwnerOrCoWorker(permissions.BasePermission):
    message = 'Editing this field is restricted to the owners only'

    def has_object_permission(self, request, view, obj):
        # Only allow read permissions to members of the project
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only allow write permissions to members involved in the task
        if obj.members.filter(user_profile=request.user.id).exists():
            return True

        return False


class PostReadAndWritePermission(permissions.BasePermission):
    message = 'Editing posts is restricted to the poster only'

    def has_object_permission(self, request, view, obj):
        # Only allow read permissions for members of the project
        if request.method in permissions.SAFE_METHODS:
            return True

        # Only allow write permissions to project manager
        user = get_object_or_404(CustomUser, username=request.user)
        query_set = Member.objects.filter(
            user=user, project=obj.id, project_manager=True)
        if query_set.exists():
            return True

        return False


class PostsViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [PostReadAndWritePermission]

    def get_queryset(self):
        '''Gets list of posts in the system

        Returns:
            list(post)
        '''
        
        queryset = Post.objects.all()
        return queryset


class MyAccountViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        '''Gets logged in user's details

        Returns:
            list(user)
        '''
        user = get_object_or_404(CustomUser, username=self.request.user)
        return user


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class UserInterestsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all().prefetch_related(
        'customuser_set'
    ).all()

    serializer_class = TagSerializer

    def get_queryset(self, *args, **kwargs):
        user_id = self.kwargs.get('user_pk')
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise NotFound('A user with this id does not exist')
        return self.queryset.filter(customuser=user)