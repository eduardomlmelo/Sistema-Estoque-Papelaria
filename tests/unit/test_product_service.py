import pytest
from src.database.connection import DatabaseConnection
from src.database.repository import ProductRepository, StockMovementRepository
from src.services.product_service import ProductService
from src.models.product import Product


@pytest.fixture
def service() -> ProductService:
    """Cria instância do ProductService para testes."""
    db = DatabaseConnection(":memory:")
    db.initialize_schema()
    product_repo = ProductRepository(db)
    movement_repo = StockMovementRepository(db)
    return ProductService(product_repo, movement_repo)


class TestProductServiceAddProduct:
    """Testes para adicionar produtos."""

    def test_add_valid_product(self, service: ProductService) -> None:
        """Testa adição de produto válido."""
        product = Product(
            name="Caderno",
            code="CAD-001",
            quantity=10,
            price=12.50,
            category="Cadernos",
            description="Descrição",
        )

        success, msg = service.add_product(product)

        assert success is True
        assert "cadastrado" in msg

    def test_add_invalid_product_empty_name(self, service: ProductService) -> None:
        """Testa adição de produto com nome vazio."""
        product = Product(
            name="",
            code="CAD-001",
            quantity=10,
            price=12.50,
            category="Cadernos",
            description="",
        )

        success, msg = service.add_product(product)

        assert success is False
        assert "Nome" in msg

    def test_add_invalid_product_negative_price(self, service: ProductService) -> None:
        """Testa adição de produto com preço negativo."""
        product = Product(
            name="Caderno",
            code="CAD-001",
            quantity=10,
            price=-5.0,
            category="Cadernos",
            description="",
        )

        success, msg = service.add_product(product)

        assert success is False
        assert "Preço" in msg

    def test_add_duplicate_code(self, service: ProductService) -> None:
        """Testa adição de produto com código duplicado."""
        product1 = Product(
            name="Caderno",
            code="CAD-001",
            quantity=10,
            price=12.50,
            category="Cadernos",
            description="",
        )
        service.add_product(product1)

        product2 = Product(
            name="Outro caderno",
            code="CAD-001",
            quantity=10,
            price=15.00,
            category="Cadernos",
            description="",
        )

        success, msg = service.add_product(product2)

        assert success is False
        assert "Erro" in msg


class TestProductServiceGetProduct:
    """Testes para recuperar produtos."""

    def test_get_existing_product(self, service: ProductService) -> None:
        """Testa obtenção de produto existente."""
        product = Product(
            name="Caderno",
            code="CAD-001",
            quantity=10,
            price=12.50,
            category="Cadernos",
            description="",
        )
        service.add_product(product)

        retrieved = service.get_all_products()[0]

        assert retrieved.name == "Caderno"
        assert retrieved.code == "CAD-001"

    def test_get_nonexistent_product(self, service: ProductService) -> None:
        """Testa obtenção de produto inexistente."""
        product = service.get_product(999)
        assert product is None


class TestProductServiceUpdateProduct:
    """Testes para atualizar produtos."""

    def test_update_valid_product(self, service: ProductService) -> None:
        """Testa atualização válida."""
        product = Product(
            name="Caderno",
            code="CAD-001",
            quantity=10,
            price=12.50,
            category="Cadernos",
            description="Original",
        )
        service.add_product(product)

        retrieved = service.get_all_products()[0]
        retrieved.name = "Caderno Atualizado"
        retrieved.quantity = 20

        success, msg = service.update_product(retrieved)

        assert success is True
        assert "atualizado" in msg

    def test_update_without_id(self, service: ProductService) -> None:
        """Testa atualização sem id."""
        product = Product(
            name="Caderno",
            code="CAD-001",
            quantity=10,
            price=12.50,
            category="Cadernos",
            description="",
        )

        success, msg = service.update_product(product)

        assert success is False
        assert "sem id" in msg

    def test_update_nonexistent_product(self, service: ProductService) -> None:
        """Testa atualização de produto inexistente."""
        product = Product(
            name="Caderno",
            code="CAD-001",
            quantity=10,
            price=12.50,
            category="Cadernos",
            description="",
            id=999,
        )

        success, msg = service.update_product(product)

        assert success is False
        assert "não encontrado" in msg


class TestProductServiceDeleteProduct:
    """Testes para deletar produtos."""

    def test_delete_existing_product(self, service: ProductService) -> None:
        """Testa exclusão de produto existente."""
        product = Product(
            name="Caderno",
            code="CAD-001",
            quantity=10,
            price=12.50,
            category="Cadernos",
            description="",
        )
        service.add_product(product)

        product_id = service.get_all_products()[0].id
        success, msg = service.delete_product(product_id)

        assert success is True
        assert "removido" in msg

    def test_delete_nonexistent_product(self, service: ProductService) -> None:
        """Testa exclusão de produto inexistente."""
        success, msg = service.delete_product(999)

        assert success is False
        assert "não encontrado" in msg


class TestProductServiceSearch:
    """Testes para busca de produtos."""

    def test_search_by_name(self, service: ProductService) -> None:
        """Testa busca por nome."""
        products = [
            Product(
                name="Caderno azul",
                code="CAD-001",
                quantity=10,
                price=12.50,
                category="Cadernos",
                description="",
            ),
            Product(
                name="Caneta azul",
                code="CAN-001",
                quantity=10,
                price=2.50,
                category="Canetas",
                description="",
            ),
        ]

        for p in products:
            service.add_product(p)

        results = service.search_products("azul")

        assert len(results) == 2

    def test_search_empty_query_returns_all(self, service: ProductService) -> None:
        """Testa que busca vazia retorna todos."""
        products = [
            Product(
                name="Caderno",
                code="CAD-001",
                quantity=10,
                price=12.50,
                category="Cadernos",
                description="",
            ),
            Product(
                name="Caneta",
                code="CAN-001",
                quantity=10,
                price=2.50,
                category="Canetas",
                description="",
            ),
        ]

        for p in products:
            service.add_product(p)

        results = service.search_products("")

        assert len(results) == 2


class TestProductServiceAdjustStock:
    """Testes para ajuste de estoque."""

    def test_adjust_stock_increase(self, service: ProductService) -> None:
        """Testa aumento de estoque."""
        product = Product(
            name="Caderno",
            code="CAD-001",
            quantity=10,
            price=12.50,
            category="Cadernos",
            description="",
        )
        service.add_product(product)

        product_id = service.get_all_products()[0].id
        success, msg = service.adjust_stock(product_id, 5, "Entrada")

        assert success is True
        assert service.get_product(product_id).quantity == 15

    def test_adjust_stock_decrease(self, service: ProductService) -> None:
        """Testa diminuição de estoque."""
        product = Product(
            name="Caderno",
            code="CAD-001",
            quantity=10,
            price=12.50,
            category="Cadernos",
            description="",
        )
        service.add_product(product)

        product_id = service.get_all_products()[0].id
        success, msg = service.adjust_stock(product_id, -3, "Venda")

        assert success is True
        assert service.get_product(product_id).quantity == 7

    def test_adjust_stock_zero_fails(self, service: ProductService) -> None:
        """Testa que ajuste com zero falha."""
        product = Product(
            name="Caderno",
            code="CAD-001",
            quantity=10,
            price=12.50,
            category="Cadernos",
            description="",
        )
        service.add_product(product)

        product_id = service.get_all_products()[0].id
        success, msg = service.adjust_stock(product_id, 0, "Teste")

        assert success is False

    def test_adjust_stock_negative_result_fails(self, service: ProductService) -> None:
        """Testa que resultado negativo falha."""
        product = Product(
            name="Caderno",
            code="CAD-001",
            quantity=10,
            price=12.50,
            category="Cadernos",
            description="",
        )
        service.add_product(product)

        product_id = service.get_all_products()[0].id
        success, msg = service.adjust_stock(product_id, -20, "Teste")

        assert success is False
        assert "negativa" in msg


class TestProductServiceHistory:
    """Testes para histórico de movimentações."""

    def test_get_product_history(self, service: ProductService) -> None:
        """Testa obtenção de histórico de produto."""
        product = Product(
            name="Caderno",
            code="CAD-001",
            quantity=10,
            price=12.50,
            category="Cadernos",
            description="",
        )
        service.add_product(product)

        product_id = service.get_all_products()[0].id
        service.adjust_stock(product_id, 5, "Entrada")
        service.adjust_stock(product_id, -2, "Venda")

        history = service.get_product_history(product_id)

        assert len(history) > 0
