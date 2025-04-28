from django.urls import reverse 
from django.test import Client
import pytest
from products.models import Product


@pytest.fixture
def create_products():
    """
    Creation of products
    """
    Product.objects.create(name="Product 1", price=50.00)
    Product.objects.create(name="Product 2", price=150.00)
    Product.objects.create(name="Product 3", price=100.00)


@pytest.fixture
def client():
    """Fixture to provide a client instance."""
    return Client()


@pytest.mark.django_db
def test_filter_by_price_range(client, create_products):
    """
    Testing if the price range filter works correctly.
    The products are filtered by the min_price and max_price query parameters.
    """
    response = client.get(reverse('home'), {'min_price': 60, 'max_price': 120})

    assert response.status_code == 200
    assert 'Product 3' in [product.name for product in response.context['object_list']]
    

@pytest.mark.django_db
def test_sort_ascending(client, create_products):
    """
    Testing if the products are sorted in ascending order by price.
    The query parameter 'sort=asc' is used to sort the products in ascending order.
    """
    response = client.get(reverse('home'), {'sort': 'asc'})

    assert response.status_code == 200

    products = response.context['object_list']
    assert products[0].price == 50
    assert products[1].price == 100
    assert products[2].price == 150


@pytest.mark.django_db
def test_sort_descending(client, create_products):
    """
    Testing if the products are sorted in descending order by price.
    The query parameter 'sort=desc' is used to sort the products in descending order.
    """
    response = client.get(reverse('home'), {'sort': 'desc'})

    assert response.status_code == 200

    products = response.context['object_list']
    assert products[0].price == 150
    assert products[1].price == 100
    assert products[2].price == 50
