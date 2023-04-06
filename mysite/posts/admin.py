from django.contrib import admin
from .models import *
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter


@admin.register(Post)
class PostAdmin(PolymorphicParentModelAdmin):
    list_display = ('title',)
    list_filter = ['title']
    search_fields = ['title', 'description']
    base_model = Post
    child_models = (BlogPost, AlbumPost, VideoPost)
    list_filter = (PolymorphicChildModelFilter,)


class PostChildAdmin(PolymorphicChildModelAdmin):
    """ Base admin class for all child models """
    base_model = Post  # Optional, explicitly set here.

    # By using these `base_...` attributes instead of the regular ModelAdmin `form` and `fieldsets`,
    # the additional fields of the child models are automatically added to the admin form.
    # base_form = ...
    # base_fieldsets = (
    #     ...
    # )


@admin.register(BlogPost)
class BlogPostAdmin(PostChildAdmin):
    list_display = ('title',)
    list_filter = ['title']
    search_fields = ['title', 'description']
    base_model = BlogPost


@admin.register(AlbumPost)
class AlbumPostAdmin(PostChildAdmin):
    list_display = ('title',)
    list_filter = ['title']
    search_fields = ['title', 'description']
    base_model = AlbumPost


@admin.register(VideoPost)
class VideoPostAdmin(PostChildAdmin):
    list_display = ('title',)
    list_filter = ['title']
    search_fields = ['title', 'description']
    base_model = VideoPost


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ['name']
    search_fields = ['name',]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('file_path',)
    list_filter = ['file_path']
    search_fields = ['file_path', 'description', 'tags']


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('file_path',)
    list_filter = ['file_path']
    search_fields = ['file_path', 'description', 'tags']


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    list_filter = ['username', 'first_name', 'last_name']
    search_fields = ['first_name', 'last_name', 'username', 'email', 'phone']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'body')
    list_filter = ['user']
    search_fields = ['user', 'body']
