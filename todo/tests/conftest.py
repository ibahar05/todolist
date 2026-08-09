# todo/tests/conftest.py
import pytest
from rest_framework.test import APIClient

from account.models import User
from todo.models import Task


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def common_user():
    return User.objects.create_user(email="ibahare05@gmail.com", password="134679@xxB")


@pytest.fixture
def common_task(common_user):
    return Task.objects.create(
        user=common_user,
        title="Test task",
        is_completed=False,
    )