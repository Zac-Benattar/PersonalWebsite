# converts python model objects to json inkedId
from rest_framework.serializers import ModelSerializer
from posts.models import *


class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class AlbumPostSerializer(ModelSerializer):
    class Meta:
        model = AlbumPost
        fields = '__all__'


class BlogPostSerializer(ModelSerializer):
    class Meta:
        model = BlogPost
        fields = '__all__'


class VideoPostSerializer(ModelSerializer):
    class Meta:
        model = VideoPost
        fields = '__all__'


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

    # Not sure if this is relevant
    def create(self, validated_data):
        get_user = self.context['request'].user
        tag = super().create(validated_data)
        get_user.interests.add(tag)
        get_user.save()
        return tag

# class TaskSerializer(ModelSerializer):
#     creation_date_unix = IntegerField(source='creation_date_to_unix')
#     start_date_unix = IntegerField(source='start_date_to_unix')
#     earliest_finish_date_unix = IntegerField(source='earliest_finish_date_to_unix')
#     latest_finish_date_unix = IntegerField(source='latest_finish_date_to_unix')
#     dependent_tasks_string = CharField(source='get_dependent_tasks_string')

#     class Meta:
#         model = Task
#         exclude = ('creation_date', 'start_date', 'latest_finish')
#         read_only_fields = ('creation_date_unix', 'start_date_unix', 'earliest_finish_date_unix', 'latest_finish_date_unix', 'dependent_tasks_string')
