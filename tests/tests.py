from unittest import TestCase as UnitTestCase
from .models import Food
from mytaggit.models import Tag


class FoodTestCase(UnitTestCase):

    def test_slug(self):
        food = Food.objects.create()
        food.tags.add('沖縄')
        self.assertEqual(1, Tag.objects.count())
        tag = food.tags.first()
        self.assertEqual(tag.slug, 'okinawa')

    def test_unique_slug(self):
        food = Food.objects.create()
        food.tags.add(
            '無常', '無情',
        )
        tags = list(food.tags.all())
        self.assertTrue(tags[1].slug.startswith(tags[0].slug))

    def test_user(self):
        from django.contrib.auth.models import User
        users = [
            User.objects.create(
                username=f'test{i}', email=f"test{1}@localhost")
            for i in range(3)]
        tags = ['野菜', '美味しい']
        food = Food.objects.create()
        food.tags.add_users(tags, users=[users])
        #
        self.assertTrue(
            Tag.objects.filter(
                name='野菜', 
                mytaggit_taggeditem_items__users__username='test1').exists())
        self.assertFalse(
            Tag.objects.filter(
                name='野菜', 
                mytaggit_taggeditem_items__users__username='test3').exists())