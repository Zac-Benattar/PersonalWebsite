from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


def get_today_datetime():
    return timezone.now()


def get_in_hour_datetime():
    return timezone.now() + timezone.timedelta(hours=1)


def get_in_day_datetime():
    return timezone.now() + timezone.timedelta(days=1)


def get_in_week_datetime():
    return timezone.now() + timezone.timedelta(days=7)

# Is this really what I want to do?
def create_post(sender, instance, created, **kwargs):
    """
    Post save handler to create/update post instances when
    BlogPost, AlbumPost, VideoPost are created/updated
    """
    content_type = ContentType.objects.get_for_model(instance)
    try:
        post= Post.objects.get(content_type=content_type,
                             object_id=instance.id)
    except Post.DoesNotExist:
        post = Post(content_type=content_type, object_id=instance.id)
    post.created = instance.created
    post.series = instance.series
    post.save()


class Post(models.Model):
    name = models.CharField(max_length=100, unique=True)
    tags = models.ManyToManyField('Tag', blank=True)
    description = models.TextField()
    comments = models.ManyToManyField('Comment', blank=True)
    poster = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    posted_date = models.DateTimeField(default=get_today_datetime)
    modified_date = models.DateTimeField(default=get_today_datetime)
    
    # Stuff to make Content Types work
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created = models.DateTimeField()
    
    class Meta:
        abstract = True
        ordering = ['-created']

    def __str__(self):
        '''Gets string representation of the post object
        Format: <post.content_object> - <post.created.date>

        Returns:
            str string representation of the image
        '''
        return "{0} - {1}".format(self.content_object.series,
                                  self.created.date())


class BlogPost(Post):
    title = models.CharField(max_length=300, unique=True)
    body = models.TextField()
    image_paths = models.ManyToManyField('Image')


class AlbumPost(Post):
    title = models.CharField(max_length=300, unique=True)
    image_paths = models.ManyToManyField('Image')


class VideoPost(Post):
    title = models.CharField(max_length=300, unique=True)
    video_path = models.ManyToManyField('Image')


class Image(models.Model):
    # This is a charfield as images should be directly uploaded to the server rather than handled by the measly server running this webapp
    # Simply saving the url of the image to be accessed later
    file_path = models.CharField(max_length=100, unique=True)

    def __str__(self):
        '''Gets string representation of the image object
        Format: <image.filePath>

        Returns:
            str string representation of the image
        '''
        return self.file_path


class Video(models.Model):
    # This is a charfield as videos should be directly uploaded to the server rather than handled by the measly server running this webapp
    # Simply saving the url of the video to be accessed later
    file_path = models.CharField(max_length=100, unique=True)

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
