from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class SignupViewTests(TestCase):
    def setUp(self):
        # django-allauth urls
        self.signup_url = reverse('account_signup')
        self.login_url = reverse('account_login')

    def test_successful_signup(self):
        payload = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'a-Strong_password-123',
            'password2': 'a-Strong_password-123',
        }
        response = self.client.post(self.signup_url, payload)
        # allauth generally redirects after successful signup (could be to email verification or profile)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_existing_username(self):
        User.objects.create_user(username='testuser', email='first@example.com', password='password123')
        payload = {
            'username': 'testuser',
            'email': 'another@example.com',
            'password1': 'a-Strong_password-123',
            'password2': 'a-Strong_password-123',
        }
        response = self.client.post(self.signup_url, payload)
        self.assertEqual(response.status_code, 200)
        # error should be rendered; content check depends on allauth locale/messages
        self.assertContains(response, 'A user with that username already exists', status_code=200)
        self.assertFalse(User.objects.filter(email='another@example.com').exclude(username='testuser').exists())

    def test_mismatched_passwords(self):
        payload = {
            'username': 'testuser2',
            'email': 'test2@example.com',
            # Use strong enough passwords so mismatch is the primary error
            'password1': 'StrongPass-12345',
            'password2': 'StrongPass-12346',
        }
        response = self.client.post(self.signup_url, payload)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You must type the same password each time', status_code=200)
        self.assertFalse(User.objects.filter(username='testuser2').exists())

    def test_invalid_email(self):
        payload = {
            'username': 'testuser3',
            'email': 'not-an-email',
            'password1': 'a-Strong_password-123',
            'password2': 'a-Strong_password-123',
        }
        response = self.client.post(self.signup_url, payload)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enter a valid email address', status_code=200)
        self.assertFalse(User.objects.filter(username='testuser3').exists())

    def test_blank_fields(self):
        response = self.client.post(self.signup_url, {})
        self.assertEqual(response.status_code, 200)
        # Should contain some error markers
        self.assertContains(response, 'This field is required', status_code=200)


class LoginViewTests(TestCase):
    def setUp(self):
        self.login_url = reverse('account_login')
        self.user = User.objects.create_user(username='testuser', email='u@example.com', password='password123')
        # A protected view in this app is 'home'
        self.protected_url = reverse('home')

    def test_successful_login_and_redirect(self):
        response = self.client.post(self.login_url, {
            'login': 'testuser',  # allauth accepts username or email as "login"
            'password': 'password123',
        })
        self.assertEqual(response.status_code, 302)
        # Attempt to reach protected page after login
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dashboard', status_code=200)

    def test_incorrect_password(self):
        response = self.client.post(self.login_url, {
            'login': 'testuser',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'The username and/or password you specified are not correct', status_code=200)

    def test_nonexistent_user(self):
        response = self.client.post(self.login_url, {
            'login': 'noone',
            'password': 'whatever',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'The username and/or password you specified are not correct', status_code=200)

    def test_unauthenticated_redirect_to_login(self):
        response = self.client.get(self.protected_url)
        # login_required redirects to login page
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('account_login'), response['Location'])

    def test_authenticated_access_to_protected_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dashboard', status_code=200)
