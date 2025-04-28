from django.urls import reverse
from django.test import Client
from products.models import Product

import pytest


@pytest.fixture
def create_products():
    """
    Creation of products
    """
    Product.objects.create(name="Product1", image="img1.jpg", description="Desc1", price=10.00)
    Product.objects.create(name="Product2", image="img2.jpg", description="Desc2", price=20.00)
    Product.objects.create(name="Product3", image="img3.jpg", description="Desc3", price=30.00)
    Product.objects.create(name="Product4", image="img4.jpg", description="Desc4", price=40.00)


@pytest.fixture
def client():
    """Fixture to provide a client instance."""
    return Client()


@pytest.mark.django_db
def test_ui_contains_filter_and_sort_fields(client):
    """
    Integration test to ensure that the UI contains price filter fields and the sort dropdown.
    """
    response = client.get(reverse('home'))
    content = response.content.decode()

    assert 'name="min_price"' in content
    assert 'name="max_price"' in content
    assert 'name="sort"' in content
    assert '<option value="asc"' in content
    assert '<option value="desc"' in content
    assert 'Apply' in content


@pytest.mark.django_db
def test_combined_price_filter_and_sort(client, setup_products):
    """
    Integration test to verify filtering by price range and sorting works correctly together.
    """

    response = client.get(reverse('home'), {
        'min_price': 15,
        'max_price': 35,
        'sort': 'asc'
    })
    content = response.content.decode()

    assert "Product1" not in content
    assert "Product2" in content
    assert "Product3" in content
    assert "Product4" not in content

    first = content.find("Product2")
    second = content.find("Product3")
    assert first < second


@pytest.mark.django_db
def test_sort_descending(client, setup_products):
    """
    Integration test to verify sorting alone works in descending order.
    """
    response = client.get(reverse('home'), {'sort': 'desc'})
    content = response.content.decode()

    pos_4 = content.find("Product4")
    pos_3 = content.find("Product3")
    pos_2 = content.find("Product2")
    pos_1 = content.find("Product1")

    assert pos_4 < pos_3 < pos_2 < pos_1


@pytest.mark.django_db
def test_sort_ascending(client, setup_products):
    """
    Integration test to verify sorting alone works in ascending order.
    """
    response = client.get(reverse('home'), {'sort': 'asc'})
    content = response.content.decode()

    pos_1 = content.find("Product1")
    pos_2 = content.find("Product2")
    pos_3 = content.find("Product3")
    pos_4 = content.find("Product4")

    assert pos_1 < pos_2 < pos_3 < pos_4