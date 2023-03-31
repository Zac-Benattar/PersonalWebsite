from django.contrib import admin
from .models import *


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ['name']
    search_fields = ['name', 'description']


class AlbumPostAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ['name']
    search_fields = ['name', 'description']


class VideoPostAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ['name']
    search_fields = ['name', 'description']


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ['name']
    search_fields = ['name',]


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    list_filter = ['username', 'first_name', 'last_name']
    search_fields = ['first_name', 'last_name', 'username', 'email', 'phone']


admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(AlbumPost, AlbumPostAdmin)
admin.site.register(VideoPost, VideoPostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
