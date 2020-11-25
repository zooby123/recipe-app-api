from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating new user with an email is successful"""
        email = 'zed-786@hotmail.com'
        password = 'password123'

        user = get_user_model().objects.create_user(
        email=email,
        password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalised"""
        email = 'zed-786@HOTMAIL.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqueal(user.email, email.lower())
