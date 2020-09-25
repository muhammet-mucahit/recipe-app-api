from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer

User = get_user_model()

INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientsApiTestCase(TestCase):
    """Test the publicly available ingredients API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving tags"""
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTestCase(TestCase):
    """Test the authorized user ingredients API"""

    def setUp(self):
        self.user = User.objects.create(
            email='test@example.com',
            password='root1234'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving tags"""
        Ingredient.objects.create(user=self.user, name='Cucumber')
        Ingredient.objects.create(user=self.user, name='Yogurt')

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test that ingredients returned are for the authenticated user"""
        user2 = User.objects.create(
            email='test2@example.com',
            password='test_password'
        )
        Ingredient.objects.create(user=user2, name='Vinegar')
        Ingredient.objects.create(user=self.user, name='Turmeric')

        res = self.client.get(INGREDIENTS_URL)

        tags = Ingredient.objects.filter(user=self.user).order_by('-name')
        serializer = IngredientSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_create_ingredient_successful(self):
        """Test creating a new ingredient"""
        ingredient_data = {'name': 'Peanut Butter'}
        res = self.client.post(INGREDIENTS_URL, data=ingredient_data)

        exists = Ingredient.objects.filter(
            user=self.user,
            name=ingredient_data['name']
        ).exists()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """Test creating a new ingredient with invalid payload"""
        ingredient_data = {'name': ''}
        res = self.client.post(INGREDIENTS_URL, data=ingredient_data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
