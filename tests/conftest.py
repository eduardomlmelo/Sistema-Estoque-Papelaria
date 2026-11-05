import pytest
from src.models.product import Product


@pytest.fixture
def sample_product() -> Product:
    """Cria um produto de exemplo para testes."""
    return Product(
        name="Caderno 200 folhas",
        code="CAD-001",
        quantity=50,
        price=12.50,
        category="Cadernos",
        description="Caderno espiral com 200 folhas pautadas",
    )


@pytest.fixture
def sample_product_with_id() -> Product:
    """Cria um produto com id para testes."""
    return Product(
        name="Caneta azul",
        code="CAN-001",
        quantity=100,
        price=2.50,
        category="Canetas",
        description="Caneta esferográfica azul",
        id=1,
    )
