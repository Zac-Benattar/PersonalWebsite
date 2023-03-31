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


class ImageAdmin(admin.ModelAdmin):
    list_display = ('file_path',)
    list_filter = ['file_path']
    search_fields = ['file_path','description','tags']


class VideoAdmin(admin.ModelAdmin):
    list_display = ('file_path',)
    list_filter = ['file_path']
    search_fields = ['file_path','description','tags']


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    list_filter = ['username', 'first_name', 'last_name']
    search_fields = ['first_name', 'last_name', 'username', 'email', 'phone']


admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(AlbumPost, AlbumPostAdmin)
admin.site.register(VideoPost, VideoPostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
