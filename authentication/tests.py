from django.contrib.auth import get_user_model
from django.test import TestCase


class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(username='Alex', password='foo')
        self.assertEqual(user.username, 'Alex')
        # self.assertIsNone(user.username, 'alex')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        # with self.assertRaises(TypeError):
        #     User.objects.create_user(username='約翰', password='foo')
        # with self.assertRaises(TypeError):
        #     User.objects.create_user(username='joão', password='foo')
        # with self.assertRaises(TypeError):
        #     User.objects.create_user(username='Джон', password='foo')

        with self.assertRaises(TypeError):
            User.objects.create_user(username='')
        with self.assertRaises(ValueError):
            User.objects.create_user(username='', password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(username='admin', password='foo')
        self.assertEqual(admin_user.username, 'admin')
        # self.assertIsNone(admin_user.username, 'Admin')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                username='administrator', password='foo', is_superuser=False)
