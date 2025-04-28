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
def test_home_page_displays_all_products(client, create_products):
    """
    Integration test: Ensure that the home page displays all products created.
    """
    response = client.get(reverse('home'))
    assert response.status_code == 200
    products = response.context['object_list']
    assert len(products) == 4
    product_names = [product.name for product in products]
    assert "Product1" in product_names
    assert "Product2" in product_names
    assert "Product3" in product_names
    assert "Product4" in product_names


@pytest.mark.django_db
def test_price_filter_combined_with_sort(client, create_products):
    """
    Integration test: Filter products by minimum price and sort them in ascending order.
    """
    response = client.get(reverse('home'), {'min_price': 15, 'sort': 'asc'})
    assert response.status_code == 200
    products = response.context['object_list']
    
    # Only Product2 (20), Product3 (30), Product4 (40) should remain
    assert len(products) == 3
    assert products[0].price == 20.00
    assert products[1].price == 30.00
    assert products[2].price == 40.00


@pytest.mark.django_db
def test_product_detail_view(client, create_products):
    """
    Integration test: Accessing the detail page of a product should return 200 and correct product info.
    """
    product = Product.objects.get(name="Product2")
    response = client.get(reverse('product_detail', args=[product.id]))
    
    assert response.status_code == 200
    assert response.context['product'].name == "Product2"
    assert response.context['product'].price == 20.00


@pytest.mark.django_db
def test_invalid_product_detail_view(client):
    """
    Integration test: Accessing a detail page with invalid ID should return 404.
    """
    response = client.get(reverse('product_detail', args=[9999]))  # ID that does not exist
    assert response.status_code == 404
