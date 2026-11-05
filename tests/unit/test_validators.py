import pytest
from src.utils.validators import (
    validate_product_name,
    validate_code,
    validate_quantity,
    validate_price,
    validate_category,
    validate_product,
)
from src.models.product import Product


class TestProductNameValidator:
    """Testes para validação de nome de produto."""

    def test_valid_name(self) -> None:
        """Testa nome válido."""
        is_valid, msg = validate_product_name("Caderno")
        assert is_valid is True
        assert msg == ""

    def test_empty_name(self) -> None:
        """Testa nome vazio."""
        is_valid, msg = validate_product_name("")
        assert is_valid is False
        assert "vazio" in msg

    def test_whitespace_only_name(self) -> None:
        """Testa nome com apenas espaços."""
        is_valid, msg = validate_product_name("   ")
        assert is_valid is False
        assert "vazio" in msg

    def test_name_too_short(self) -> None:
        """Testa nome muito curto."""
        is_valid, msg = validate_product_name("Ca")
        assert is_valid is False
        assert "3 caracteres" in msg

    def test_name_too_long(self) -> None:
        """Testa nome muito longo."""
        is_valid, msg = validate_product_name("A" * 101)
        assert is_valid is False
        assert "100 caracteres" in msg


class TestCodeValidator:
    """Testes para validação de código."""

    def test_valid_code(self) -> None:
        """Testa código válido."""
        is_valid, msg = validate_code("CAD-001")
        assert is_valid is True
        assert msg == ""

    def test_empty_code(self) -> None:
        """Testa código vazio."""
        is_valid, msg = validate_code("")
        assert is_valid is False
        assert "vazio" in msg

    def test_code_too_short(self) -> None:
        """Testa código muito curto."""
        is_valid, msg = validate_code("AB")
        assert is_valid is False
        assert "3 caracteres" in msg

    def test_code_too_long(self) -> None:
        """Testa código muito longo."""
        is_valid, msg = validate_code("A" * 21)
        assert is_valid is False
        assert "20 caracteres" in msg


class TestQuantityValidator:
    """Testes para validação de quantidade."""

    def test_valid_quantity(self) -> None:
        """Testa quantidade válida."""
        is_valid, msg = validate_quantity(10)
        assert is_valid is True
        assert msg == ""

    def test_zero_quantity_valid(self) -> None:
        """Testa que zero é válido."""
        is_valid, msg = validate_quantity(0)
        assert is_valid is True

    def test_negative_quantity(self) -> None:
        """Testa quantidade negativa."""
        is_valid, msg = validate_quantity(-5)
        assert is_valid is False
        assert "negativa" in msg

    def test_float_quantity_invalid(self) -> None:
        """Testa que float é inválido."""
        is_valid, msg = validate_quantity(10.5)  # type: ignore
        assert is_valid is False
        assert "inteiro" in msg


class TestPriceValidator:
    """Testes para validação de preço."""

    def test_valid_price(self) -> None:
        """Testa preço válido."""
        is_valid, msg = validate_price(12.50)
        assert is_valid is True
        assert msg == ""

    def test_valid_integer_price(self) -> None:
        """Testa que inteiro é válido para preço."""
        is_valid, msg = validate_price(10)
        assert is_valid is True

    def test_zero_price_valid(self) -> None:
        """Testa que zero é válido."""
        is_valid, msg = validate_price(0.0)
        assert is_valid is True

    def test_negative_price(self) -> None:
        """Testa preço negativo."""
        is_valid, msg = validate_price(-5.0)
        assert is_valid is False
        assert "negativo" in msg

    def test_price_too_high(self) -> None:
        """Testa preço muito alto."""
        is_valid, msg = validate_price(1000000.0)
        assert is_valid is False
        assert "999999.99" in msg

    def test_string_price_invalid(self) -> None:
        """Testa que string é inválida."""
        is_valid, msg = validate_price("10")  # type: ignore
        assert is_valid is False
        assert "número" in msg


class TestCategoryValidator:
    """Testes para validação de categoria."""

    def test_valid_category(self) -> None:
        """Testa categoria válida."""
        is_valid, msg = validate_category("Cadernos")
        assert is_valid is True
        assert msg == ""

    def test_empty_category(self) -> None:
        """Testa categoria vazia."""
        is_valid, msg = validate_category("")
        assert is_valid is False
        assert "vazia" in msg

    def test_category_too_short(self) -> None:
        """Testa categoria muito curta."""
        is_valid, msg = validate_category("AB")
        assert is_valid is False
        assert "3 caracteres" in msg

    def test_category_too_long(self) -> None:
        """Testa categoria muito longa."""
        is_valid, msg = validate_category("A" * 51)
        assert is_valid is False
        assert "50 caracteres" in msg


class TestProductValidator:
    """Testes para validação completa de produto."""

    def test_valid_product(self) -> None:
        """Testa validação de produto válido."""
        product = Product(
            name="Caderno",
            code="CAD-001",
            quantity=10,
            price=12.50,
            category="Cadernos",
            description="Descrição",
        )
        is_valid, errors = validate_product(product)
        assert is_valid is True
        assert len(errors) == 0

    def test_multiple_errors(self) -> None:
        """Testa que múltiplos erros são reportados."""
        product = Product(
            name="",
            code="",
            quantity=-5,
            price=-10.0,
            category="",
            description="",
        )
        is_valid, errors = validate_product(product)
        assert is_valid is False
        assert len(errors) > 0
        assert len(errors) == 5
