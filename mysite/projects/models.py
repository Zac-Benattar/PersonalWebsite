from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone


def get_today_datetime():
    return timezone.now()


def get_in_hour_datetime():
    return timezone.now() + timezone.timedelta(hours=1)


def get_in_day_datetime():
    return timezone.now() + timezone.timedelta(days=1)


def get_in_week_datetime():
    return timezone.now() + timezone.timedelta(days=7)


class Content(models.Model):
    name = models.CharField(max_length=100, unique=True)
    tags = models.ForeignKey('Tag', on_delete=models.CASCADE)
    description = models.TextField()
    comments = models.ManyToManyField('Comment')

    def __str__(self):
        '''Gets string representation of the content object
        Format: <content.name>

        Returns:
            str string representation of the content
        '''
        return self.name


class BlogPost(Content):
    title = models.CharField(max_length=300, unique=True)
    body = models.TextField()
    imagePaths = models.ManyToManyField('Image')


class AlbumPost(Content):
    title = models.CharField(max_length=300, unique=True)
    imagePaths = models.ManyToManyField('Image')


class VideoPost(Content):
    title = models.CharField(max_length=300, unique=True)
    videoPath = models.ManyToManyField('Image')


class Image(models.Model):
    # This is a charfield as images should be directly uploaded to the server rather than handled by the measly server running this webapp
    # Simply saving the url of the image to be accessed later
    filePath = models.CharField(max_length=100, unique=True)

    def __str__(self):
        '''Gets string representation of the image object
        Format: <image.filePath>

        Returns:
            str string representation of the image
        '''
        return self.filePath


class Video(models.Model):
    # This is a charfield as videos should be directly uploaded to the server rather than handled by the measly server running this webapp
    # Simply saving the url of the video to be accessed later
    filePath = models.CharField(max_length=100, unique=True)

    def __str__(self):
        '''Gets string representation of the video object
        Format: <video.filePath>

        Returns:
            str string representation of the video
        '''
        return self.filePath

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
        return len(Content.objects.filter(tags=self))

    def get_content(self):
        '''Gets content objects with the tag

        Returns:
            list list of content objects with the tag
        '''
        return Content.objects.filter(tags=self)


class Comment(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    body = models.TextField()

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

    def __str__(self):
        '''Gets string representation of the custom user object
        Format: <customuser.username>

        Returns:
            str string representation of the custom user
        '''
        return self.username
