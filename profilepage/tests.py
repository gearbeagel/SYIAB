import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="password123")


@pytest.fixture
def api_client():
    return APIClient()


def test_view_profile(client, user):
    url = reverse('view_profile', kwargs={'username': user.username})
    response = client.get(url)
    assert response.status_code == 200
    assert 'profile_picture' in response.context
    assert 'motivation' in response.context


def test_edit_profile(client, user):
    client.login(username=user.username, password="password123")
    url = reverse('edit_profile', kwargs={'username': user.username})
    response = client.post(url, {'username': 'newuser'})
    assert response.status_code == 302  # Expecting redirect
    user.refresh_from_db()
    assert user.username == 'newuser'


def test_delete_profile(client, user):
    client.login(username=user.username, password="password123")
    url = reverse('delete_profile', kwargs={'username': user.username})
    response = client.post(url)
    assert response.status_code == 302
    assert not User.objects.filter(username='testuser').exists()


def test_api_retrieve_profile(api_client, user):
    url = reverse('profile-detail', kwargs={'pk': user.username})
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data['username'] == user.username
    assert 'motivation' in response.data


def test_api_edit_profile(api_client, user):
    api_client.force_authenticate(user=user)
    url = reverse('profile-edit', kwargs={'pk': user.username})
    response = api_client.put(url, {'username': 'updateduser'}, format='json')
    assert response.status_code == 200
    user.refresh_from_db()
    assert user.username == 'updateduser'


def test_api_delete_profile(api_client, user):
    api_client.force_authenticate(user=user)
    url = reverse('profile-delete', kwargs={'pk': user.username})
    response = api_client.delete(url)
    assert response.status_code == 204
    assert not User.objects.filter(username=user.username).exists()
