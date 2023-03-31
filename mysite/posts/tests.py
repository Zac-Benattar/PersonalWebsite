from django.test import TestCase
from projects.models import *


class tester(TestCase):

    # Setting up the test data

    def setUp(self):

        # Creating a tag
        tag1 = Tag.objects.create(name="AI")

        # Creating a blog post
        blog_post1 = BlogPost.objects.create(
            name="BlogPost1", description="Blog post about a thing", title="Title of blog post", body="Body of blog post")
        blog_post1.tags.add(tag1)

        # Creating a user
        user1 = CustomUser.objects.create(phone='+15555555555')
        user1.interests.add(tag1)

    # Testing the system

    # Tests that the system returns all posts with a given tag
    # This is yet to be run lol, it may not even work
    def test_number_of_posts_about_tag(self):
        example_tag = Tag.objects.get('tag1')
        testData = example_tag.get_content_count()
        self.assertEqual(testData, Post.objects.filter(tags__in=Tag.objects.get(
            'tag1')), 'The function returned an incorrect number of posts.')
