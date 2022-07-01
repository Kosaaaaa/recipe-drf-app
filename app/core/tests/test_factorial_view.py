"""
Tests for the factorial view API.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient


def factorial_url(n: int):
    """Create and return an ingredient detail URL."""
    return reverse('factorial', args=[n])


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class AnonFactorialViewTest(TestCase):
    """
    Anonymous Tests for the factorial view API.
    """

    def setUp(self) -> None:
        self.client = APIClient()

    def test_anon_throttling(self):
        res = self.client.get(factorial_url(5))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['result'], 120)

        res = self.client.get(factorial_url(5))
        self.assertEqual(res.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class AuthFactorialViewTest(TestCase):
    """
        Authenticated Tests for the factorial view API.
    """

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123')
        self.client.force_authenticate(self.user)

    def test_user_throttling(self):
        for _ in range(10):
            res = self.client.get(factorial_url(5))
            self.assertEqual(res.status_code, status.HTTP_200_OK)

        res = self.client.get(factorial_url(5))
        self.assertEqual(res.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
