from django.contrib.auth.models import User
from django.test import TestCase
from blogs.models import Blog, Post, Category
from datetime import datetime

# Create your tests here.
class TestBlogsFeatures(TestCase):

    def setUp(self):
        self.users = {
            'red': User.objects.create(username='red', email='red@pokemon.es', password='charmander'),
            'green': User.objects.create(username='green', email='green@pokemon.es', password='bulbasaur')
        }

        self.category = Category.objects.create(name='Sample', description='I\'s only a stupid sample')
        self.blog = Blog.objects.create(title='Blog of Red', owner=self.users['red'], description='')
        self.post = Post.objects.create(title='Sample Post', content='Sample post @with a @mention to @green',
                                        publish_date=datetime.now(), blog=self.blog, category=self.category)

    def test_get_mentions_from_post_content(self):
        self.assertEqual(len(self.post.get_users_mentioned_on_post()), 1)

    def test_if_green_is_in_mentioned_users(self):
        self.assertTrue(self.users['green'] in self.post.get_users_mentioned_on_post())
