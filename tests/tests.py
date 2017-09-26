# coding: utf-8
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
