import pytest
import sqlite3
from datetime import datetime
from src.database.connection import DatabaseConnection
from src.database.repository import ProductRepository, StockMovementRepository
from src.models.product import Product
from src.models.stock_movement import StockMovement


@pytest.fixture
def db_connection() -> DatabaseConnection:
    """Cria conexão com banco de dados em memória para testes."""
    connection = DatabaseConnection(":memory:")
    connection.initialize_schema()
    yield connection
    connection.close()


@pytest.fixture
def product_repo(db_connection: DatabaseConnection) -> ProductRepository:
    """Cria repositório de produtos com banco de teste."""
    return ProductRepository(db_connection)


@pytest.fixture
def movement_repo(db_connection: DatabaseConnection) -> StockMovementRepository:
    """Cria repositório de movimentações com banco de teste."""
    return StockMovementRepository(db_connection)


class TestProductRepository:
    """Testes do repositório de produtos."""

    def test_create_product(self, product_repo: ProductRepository) -> None:
        """Testa criação de um produto."""
        product = Product(
            name="Caderno",
            code="CAD-001",
            quantity=10,
            price=12.50,
            category="Cadernos",
            description="Caderno espiral",
        )

        created = product_repo.create(product)

        assert created.id is not None
        assert created.name == "Caderno"
        assert created.created_at is not None
        assert created.updated_at is not None

    def test_read_product_by_id(self, product_repo: ProductRepository) -> None:
        """Testa leitura de produto por id."""
        product = Product(
            name="Caderno",
            code="CAD-001",
            quantity=10,
            price=12.50,
            category="Cadernos",
            description="Caderno espiral",
        )
        created = product_repo.create(product)

        retrieved = product_repo.read(created.id)

        assert retrieved is not None
        assert retrieved.name == "Caderno"
        assert retrieved.code == "CAD-001"

    def test_read_nonexistent_product(self, product_repo: ProductRepository) -> None:
        """Testa leitura de produto inexistente."""
        retrieved = product_repo.read(999)
        assert retrieved is None

    def test_read_product_by_code(self, product_repo: ProductRepository) -> None:
        """Testa leitura de produto por código."""
        product = Product(
            name="Caderno",
            code="CAD-001",
            quantity=10,
            price=12.50,
            category="Cadernos",
            description="Caderno espiral",
        )
        product_repo.create(product)

        retrieved = product_repo.read_by_code("CAD-001")

        assert retrieved is not None
        assert retrieved.name == "Caderno"

    def test_read_all_products(self, product_repo: ProductRepository) -> None:
        """Testa leitura de todos os produtos."""
        for i in range(3):
            product = Product(
                name=f"Produto {i}",
                code=f"PROD-{i:03d}",
                quantity=10,
                price=10.00,
                category="Categoria",
                description="Descrição",
            )
            product_repo.create(product)

        all_products = product_repo.read_all()

        assert len(all_products) == 3

    def test_search_products_by_name(self, product_repo: ProductRepository) -> None:
        """Testa busca de produtos por nome."""
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
                name="Caderno vermelho",
                code="CAD-002",
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

        for product in products:
            product_repo.create(product)

        results = product_repo.search("azul")

        assert len(results) == 2
        assert any(p.name == "Caderno azul" for p in results)
        assert any(p.name == "Caneta azul" for p in results)

    def test_search_products_by_code(self, product_repo: ProductRepository) -> None:
        """Testa busca de produtos por código."""
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

        for product in products:
            product_repo.create(product)

        results = product_repo.search("CAD")

        assert len(results) == 1
        assert results[0].code == "CAD-001"

    def test_update_product(self, product_repo: ProductRepository) -> None:
        """Testa atualização de produto."""
        product = Product(
            name="Caderno",
            code="CAD-001",
            quantity=10,
            price=12.50,
            category="Cadernos",
            description="Descrição original",
        )
        created = product_repo.create(product)

        created.name = "Caderno Atualizado"
        created.quantity = 20
        updated = product_repo.update(created)

        assert updated is True

        retrieved = product_repo.read(created.id)
        assert retrieved.name == "Caderno Atualizado"
        assert retrieved.quantity == 20

    def test_delete_product(self, product_repo: ProductRepository) -> None:
        """Testa exclusão de produto."""
        product = Product(
            name="Caderno",
            code="CAD-001",
            quantity=10,
            price=12.50,
            category="Cadernos",
            description="",
        )
        created = product_repo.create(product)

        deleted = product_repo.delete(created.id)

        assert deleted is True

        retrieved = product_repo.read(created.id)
        assert retrieved is None

    def test_create_duplicate_code_raises_error(
        self, product_repo: ProductRepository
    ) -> None:
        """Testa que código duplicado gera erro."""
        product1 = Product(
            name="Caderno 1",
            code="CAD-001",
            quantity=10,
            price=12.50,
            category="Cadernos",
            description="",
        )
        product_repo.create(product1)

        product2 = Product(
            name="Caderno 2",
            code="CAD-001",
            quantity=10,
            price=12.50,
            category="Cadernos",
            description="",
        )

        with pytest.raises(sqlite3.IntegrityError):
            product_repo.create(product2)


class TestStockMovementRepository:
    """Testes do repositório de movimentações de estoque."""

    def test_log_movement(self, movement_repo: StockMovementRepository) -> None:
        """Testa registro de uma movimentação."""
        movement = StockMovement(
            product_id=1,
            quantity_change=10,
            reason="Entrada",
            timestamp=datetime.now(),
        )

        logged = movement_repo.log_movement(movement)

        assert logged.id is not None
        assert logged.quantity_change == 10

    def test_get_movements_by_product(self, movement_repo: StockMovementRepository) -> None:
        """Testa recuperação de movimentações de um produto."""
        movements = [
            StockMovement(
                product_id=1,
                quantity_change=10,
                reason="Entrada",
                timestamp=datetime.now(),
            ),
            StockMovement(
                product_id=1,
                quantity_change=-5,
                reason="Venda",
                timestamp=datetime.now(),
            ),
        ]

        for movement in movements:
            movement_repo.log_movement(movement)

        retrieved = movement_repo.get_movements_by_product(1)

        assert len(retrieved) == 2

    def test_get_all_movements(self, movement_repo: StockMovementRepository) -> None:
        """Testa recuperação de todas as movimentações."""
        for i in range(3):
            movement = StockMovement(
                product_id=i + 1,
                quantity_change=10,
                reason="Entrada",
                timestamp=datetime.now(),
            )
            movement_repo.log_movement(movement)

        all_movements = movement_repo.get_all_movements()

        assert len(all_movements) == 3
