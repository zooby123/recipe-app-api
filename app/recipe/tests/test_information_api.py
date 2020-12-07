from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Information, Recipe

from recipe.serializers import InformationSerializer


INFORMATION_URL = reverse('recipe:information-list')


class PublicInformationApiTests(TestCase):
    """Test the publically available Information API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access this endpoint"""
        res = self.client.get(INFORMATION_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateInformationAPITests(TestCase):
    """Test the private Information API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@londonappdev.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_information_list(self):
        """Test retrieving a list of Information"""
        Information.objects.create(user=self.user, name='kale')
        Information.objects.create(user=self.user, name='salt')

        res = self.client.get(INFORMATION_URL)

        information = Information.objects.all().order_by('-name')
        serializer = InformationSerializer(information, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_information_limited_to_user(self):
        """Test that Information for authenticated user are returned"""
        user2 = get_user_model().objects.create_user(
            'other@londonappdev.com',
            'testpass'
        )
        Information.objects.create(user=user2, name='Vinegar')

        information = Information.objects.create(user=self.user, name='steaks')

        res = self.client.get(INFORMATION_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], information.name)

    def test_create_information_successful(self):
        """Test creating a new information"""
        payload = {'name': 'Cabbage'}
        self.client.post(INFORMATION_URL, payload)

        exists = Information.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_information_invalid(self):
        """Test creating invalid information fails"""
        payload = {'name': ''}
        res = self.client.post(INFORMATION_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_information_assigned_to_recipes(self):
        """Test filtering Information by those assigned to recipes"""
        information1 = Information.objects.create(
            user=self.user, name='Apples'
        )
        information2 = Information.objects.create(
            user=self.user, name='Turkey'
        )
        recipe = Recipe.objects.create(
            title='Apple crumble',
            location='5',
            price='£££',
            user=self.user
        )
        recipe.information.add(information1)

        res = self.client.get(INFORMATION_URL, {'assigned_only': 1})

        serializer1 = InformationSerializer(information1)
        serializer2 = InformationSerializer(information2)
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_retrieve_information_assigned_unique(self):
        """Test filtering Information by assigned returns unique items"""
        information = Information.objects.create(user=self.user, name='Eggs')
        Information.objects.create(user=self.user, name='Cheese')
        recipe1 = Recipe.objects.create(
            title='Eggs benedict',
            location='Europe',
            price='12.00',
            user=self.user
        )
        recipe1.information.add(information)
        recipe2 = Recipe.objects.create(
            title='Green eggs on toast',
            location='Scotland',
            price='5.00',
            user=self.user
        )
        recipe2.information.add(information)

        res = self.client.get(INFORMATION_URL, {'assigned_only': 1})

        self.assertEqual(len(res.data), 1)
