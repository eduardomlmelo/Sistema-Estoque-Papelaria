import pytest
from datetime import datetime
from src.models.product import Product


@pytest.fixture
def valid_product() -> Product:
    """Cria um produto válido para testes."""
    return Product(
        name="Caderno 200 folhas",
        code="CAD-001",
        quantity=50,
        price=12.50,
        category="Cadernos",
        description="Caderno espiral com 200 folhas pautadas",
    )


class TestProductValidation:
    """Testes de validação do modelo Product."""

    def test_valid_product(self, valid_product: Product) -> None:
        """Testa se um produto válido passa na validação."""
        is_valid, message = valid_product.is_valid()
        assert is_valid is True
        assert message == ""

    def test_empty_name(self) -> None:
        """Testa validação com nome vazio."""
        product = Product(
            name="",
            code="CAD-001",
            quantity=10,
            price=12.50,
            category="Cadernos",
            description="Descrição",
        )
        is_valid, message = product.is_valid()
        assert is_valid is False
        assert "Nome" in message

    def test_whitespace_only_name(self) -> None:
        """Testa validação com nome contendo apenas espaços."""
        product = Product(
            name="   ",
            code="CAD-001",
            quantity=10,
            price=12.50,
            category="Cadernos",
            description="Descrição",
        )
        is_valid, message = product.is_valid()
        assert is_valid is False
        assert "Nome" in message

    def test_empty_code(self) -> None:
        """Testa validação com código vazio."""
        product = Product(
            name="Caderno",
            code="",
            quantity=10,
            price=12.50,
            category="Cadernos",
            description="Descrição",
        )
        is_valid, message = product.is_valid()
        assert is_valid is False
        assert "Código" in message

    def test_negative_quantity(self) -> None:
        """Testa validação com quantidade negativa."""
        product = Product(
            name="Caderno",
            code="CAD-001",
            quantity=-5,
            price=12.50,
            category="Cadernos",
            description="Descrição",
        )
        is_valid, message = product.is_valid()
        assert is_valid is False
        assert "Quantidade" in message

    def test_negative_price(self) -> None:
        """Testa validação com preço negativo."""
        product = Product(
            name="Caderno",
            code="CAD-001",
            quantity=10,
            price=-5.00,
            category="Cadernos",
            description="Descrição",
        )
        is_valid, message = product.is_valid()
        assert is_valid is False
        assert "Preço" in message

    def test_empty_category(self) -> None:
        """Testa validação com categoria vazia."""
        product = Product(
            name="Caderno",
            code="CAD-001",
            quantity=10,
            price=12.50,
            category="",
            description="Descrição",
        )
        is_valid, message = product.is_valid()
        assert is_valid is False
        assert "Categoria" in message

    def test_zero_quantity_is_valid(self) -> None:
        """Testa se quantidade zero é válida."""
        product = Product(
            name="Caderno",
            code="CAD-001",
            quantity=0,
            price=12.50,
            category="Cadernos",
            description="Descrição",
        )
        is_valid, message = product.is_valid()
        assert is_valid is True

    def test_zero_price_is_valid(self) -> None:
        """Testa se preço zero é válido (pode ser necessário para promções)."""
        product = Product(
            name="Caderno",
            code="CAD-001",
            quantity=10,
            price=0.00,
            category="Cadernos",
            description="Descrição",
        )
        is_valid, message = product.is_valid()
        assert is_valid is True

    def test_product_string_representation(self, valid_product: Product) -> None:
        """Testa a representação em string do produto."""
        result = str(valid_product)
        assert "Caderno 200 folhas" in result
        assert "CAD-001" in result
        assert "12.50" in result


class TestProductAttributes:
    """Testes de atributos e inicialização do modelo Product."""

    def test_product_with_id_and_timestamps(self) -> None:
        """Testa criação de produto com id e timestamps."""
        now = datetime.now()
        product = Product(
            name="Caderno",
            code="CAD-001",
            quantity=10,
            price=12.50,
            category="Cadernos",
            description="Descrição",
            id=1,
            created_at=now,
            updated_at=now,
        )
        assert product.id == 1
        assert product.created_at == now
        assert product.updated_at == now

    def test_product_optional_fields_default_to_none(self) -> None:
        """Testa se campos opcionais padrão para None."""
        product = Product(
            name="Caderno",
            code="CAD-001",
            quantity=10,
            price=12.50,
            category="Cadernos",
            description="Descrição",
        )
        assert product.id is None
        assert product.created_at is None
        assert product.updated_at is None
