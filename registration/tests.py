import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.timezone import now, timedelta

from boxes.models import Box

User = get_user_model()


@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(username="testuser", password="testpassword")


@pytest.mark.django_db
def test_home_view_authenticated(client, user):
    client.force_login(user)
    response = client.get(reverse('home'))
    assert response.status_code == 200
    assert 'message' in response.context


@pytest.mark.django_db
def test_home_view_boxes_display(client, user):
    client.force_login(user)
    Box.objects.create(creator=user, date_opening=now() + timedelta(days=1))
    response = client.get(reverse('home'))
    assert response.status_code == 200
    assert 'boxes' in response.context
    assert len(response.context['boxes']) == 1


@pytest.mark.django_db
def test_registration_view(client):
    response = client.post(reverse('registration'), {
        'username': 'newuser',
        'email': 'lbozo@gmail.com',
        'password1': 'TestPassword123',
        'password2': 'TestPassword123',
    })
    print(response.content.decode())
    assert response.status_code == 302
    assert User.objects.filter(username='newuser').exists()


@pytest.mark.django_db
def test_registration_view_fail(client):
    response = client.post(reverse('registration'), {
        'username': '',
        'email': 'lbozo@gmail.com',
        'password1': 'TestPassword123',
        'password2': 'TestPassword123',
    })
    assert response.status_code == 200
    assert not User.objects.filter(username='').exists()


@pytest.mark.django_db
def test_login_view_success(client, user):
    response = client.post(reverse('login'), {
        'username': user.username,
        'password': 'testpassword',
    })
    assert response.status_code == 302


@pytest.mark.django_db
def test_login_view_fail(client):
    response = client.post(reverse('login'), {
        'username': 'nonexistent',
        'password': 'wrongpassword',
    })
    assert response.status_code == 200
    assert 'Invalid username or password.' in response.content.decode()


@pytest.mark.django_db
def test_logout_view(client, user):
    client.force_login(user)
    response = client.get(reverse('logout'))
    assert response.status_code == 302
