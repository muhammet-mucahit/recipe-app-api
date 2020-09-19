from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class TestModels(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@example.com'
        password = 'TestPass123'
        user = User.objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@EXAMPLE.COM'
        user = User.objects.create_user(
            email=email,
            password='test123'
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating with no email raises error"""
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email=None,
                password='test123'
            )

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        email = 'test@example.com'
        password = 'test123'
        superuser = User.objects.create_superuser(
            email=email,
            password=password
        )

        self.assertEqual(superuser.email, email)
        self.assertTrue(superuser.check_password(password))
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)
