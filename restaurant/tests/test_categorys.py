from django.contrib.auth.models import User
from rest_framework import status
import pytest
from restaurant.models import Category
from model_bakery import baker


@pytest.fixture
def create_category(api_client):
    def do_create_category(category):
        return api_client.post('/restaurant/category/', category)
    return do_create_category


@pytest.fixture
def authenticate(api_client):
    def do_authenticate(is_staff=False):
        return api_client.force_authenticate(user=User(is_staff=is_staff))
    return do_authenticate


@pytest.mark.django_db
class TestCreateCategory:
    # @pytest.mark.skip
    def test_if_user_is_anonymous_returns_401(self, create_category):
        # Arrange

        # Act
        response = create_category({'title': 'a'})
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, authenticate, create_category):
        # Arrange

        # Act
        authenticate()
        response = create_category({'title': 'a'})
        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, authenticate, create_category):
        # Arrange

        # Act
        authenticate(True)
        response = create_category({'title': ''})
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    def test_if_data_is_valid_returns_201(self, authenticate, create_category):
        # Arrange

        # Act
        authenticate(True)
        response = create_category({'title': 'a'})
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestRetrieveCategory:
    def test_if_category_exists_return_200(self, api_client):
        # Arrange
        category = baker.make(Category)
        response = api_client.get(f'/restaurant/category/{category.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': category.id,
            'title': category.title,
            'foods_count': 0
        }
  