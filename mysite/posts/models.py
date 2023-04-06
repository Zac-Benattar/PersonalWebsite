from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from ckeditor.fields import RichTextField
from polymorphic.models import PolymorphicModel


def get_today_datetime():
    return timezone.now()


def get_in_hour_datetime():
    return timezone.now() + timezone.timedelta(hours=1)


def get_in_day_datetime():
    return timezone.now() + timezone.timedelta(days=1)


def get_in_week_datetime():
    return timezone.now() + timezone.timedelta(days=7)


class Post(PolymorphicModel):
    title = models.CharField(max_length=300, unique=True)
    tags = models.ManyToManyField('Tag', blank=True)
    description = models.TextField()
    comments = models.ManyToManyField('Comment', blank=True)
    poster = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    posted_date = models.DateTimeField(default=get_today_datetime)
    modified_date = models.DateTimeField(default=get_today_datetime)

    class Meta:
        ordering = ['-posted_date']

    def __str__(self):
        '''Gets string representation of the post object
        Format: <post.title>

        Returns:
            str string representation of the post
        '''
        return self.title


class BlogPost(Post):
    # Using a package for rich text fields, it outputs as HTML so use the safe filter in the template
    # https://django-ckeditor.readthedocs.io/en/latest/
    body = RichTextField()
    images = models.ManyToManyField('Image', blank=True)
    
    def get_post_type(self):
        return 'Blog'


class AlbumPost(Post):
    images = models.ManyToManyField('Image', blank=False)
    
    def get_post_type(self):
        return 'Album'


class VideoPost(Post):
    video = models.ForeignKey('Video', on_delete=models.CASCADE)
    
    def get_post_type(self):
        return 'Video'


class Image(models.Model):
    # This is a charfield as images should be directly uploaded to the server rather than handled by the measly server running this webapp
    # Simply saving the url of the image to be accessed later
    file_path = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField('Tag', blank=True)

    def __str__(self):
        '''Gets string representation of the image object
        Format: <image.filePath>

        Returns:
            str string representation of the image
        '''
        return self.file_path


class Video(models.Model):
    # Need to improve the default so it is unique
    title = models.CharField(
        max_length=300, unique=True, default='Untitled Video')
    # This is a charfield as videos should be directly uploaded to the server rather than handled by the measly server running this webapp
    # Simply saving the url of the video to be accessed later
    file_path = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    YOUTUBE = 'Y'
    SERVER = 'S'
    hosting_method_choices = [
        (YOUTUBE, 'YouTube'),
        (SERVER, 'Server'),
    ]
    hosting_method = models.CharField(
        max_length=1,
        choices=hosting_method_choices,
        default=YOUTUBE,
    )

    def __str__(self):
        '''Gets string representation of the video object
        Format: <video.filePath>

        Returns:
            str string representation of the video
        '''
        return self.file_path

# Tag represents a classification tag for content


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        '''Gets string representation of the tag object
        Format: <tag.name>

        Returns:
            str string representation of the tag
        '''
        return self.name

    def get_content_count(self):
        '''Gets number of content objects with the tag

        Returns:
            int number of content objects with the tag
        '''
        return len(Post.objects.filter(tags=self))

    def get_content(self):
        '''Gets content objects with the tag

        Returns:
            list list of content objects with the tag
        '''
        return Post.objects.filter(tags=self)


class Comment(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    body = models.TextField()
    posted_date = models.DateTimeField(default=get_today_datetime)
    modified_date = models.DateTimeField(default=get_today_datetime)

    def __str__(self):
        '''Gets string representation of the comment object
        Format: <comment.user>: <comment.body>

        Returns:
            str string representation of the comment
        '''
        return self.user + ": " + self.body


class CustomUser(AbstractUser):
    # Using a library for phone number, if you want the string representation use phone.as_e164
    # https://django-phonenumber-field.readthedocs.io/en/latest/
    phone = PhoneNumberField(null=False, blank=True, unique=True)
    interests = models.ManyToManyField(Tag, blank=True)
    profile_picture = models.ForeignKey(
        Image, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        '''Gets string representation of the custom user object
        Format: <customuser.username>

        Returns:
            str string representation of the custom user
        '''
        return self.username
