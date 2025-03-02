import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient
from boxes.models import Box
from django.contrib.auth import get_user_model
from datetime import timedelta

User = get_user_model()


@pytest.mark.django_db
class TestBoxViewsAndAPI:
    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def user(self, django_user_model):
        return django_user_model.objects.create_user(username="testuser", password="testpass")

    @pytest.fixture
    def auth_client(self, client, user):
        client.force_login(user)
        return client

    @pytest.fixture
    def box(self, user):
        return Box.objects.create(
            name="Test Box",
            creator=user,
            date_opening=timezone.now() + timedelta(days=10),
            category=Box.Categories.FAMILY,
        )

    def test_create_box_valid(self, auth_client):
        url = reverse("create_box")
        data = {
            "name": "New Box",
            "date_opening": timezone.now() + timedelta(days=5),
            "category": Box.Categories.LOVE,
        }

        response = auth_client.post(url, data)
        print(response.content.decode())
        assert response.status_code == 302
        assert Box.objects.filter(name="New Box").exists()

    def test_create_box_past_date(self, auth_client):
        url = reverse("create_box")
        data = {
            "name": "Invalid Box",
            "date_opening": timezone.now() - timedelta(days=1),
            "category": Box.Categories.LOVE,
        }

        response = auth_client.post(url, data)
        assert response.status_code == 200
        assert not Box.objects.filter(name="Invalid Box").exists()

    def test_view_box(self, auth_client, box):
        url = reverse("view_box", args=[box.pk])
        response = auth_client.get(url)
        assert response.status_code == 200
        assert "Test Box" in response.content.decode()

    def test_delete_box(self, auth_client, box):
        url = reverse("delete_box", args=[box.pk])
        response = auth_client.post(url)
        assert response.status_code == 302
        assert not Box.objects.filter(pk=box.pk).exists()

    def test_get_box_api(self, client, box):
        url = f"/api/boxes/{box.pk}/"
        response = client.get(url)
        assert response.status_code == 200
        assert response.json()["name"] == "Test Box"

    def test_create_box_api(self, client, user):
        url = "/api/boxes/"
        data = {
            "name": "New API Box",
            "creator": user.pk,
            "date_opening": (timezone.now() + timedelta(days=5)).isoformat(),
        }
        response = client.post(url, data, format="json")
        assert response.status_code == 201
        assert Box.objects.filter(name="New API Box").exists()

    def test_delete_box_api(self, client, box):
        url = f"/api/boxes/{box.pk}/"
        response = client.delete(url)
        assert response.status_code == 204
        assert not Box.objects.filter(pk=box.pk).exists()
