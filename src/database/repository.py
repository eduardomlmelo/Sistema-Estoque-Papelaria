from datetime import datetime
from typing import Optional
from src.database.connection import DatabaseConnection
from src.models.product import Product
from src.models.stock_movement import StockMovement


class ProductRepository:
    """Gerencia operações CRUD para produtos."""

    def __init__(self, connection: DatabaseConnection) -> None:
        """
        Inicializa o repositório.

        Args:
            connection: Gerenciador de conexão com banco de dados
        """
        self.connection = connection

    def create(self, product: Product) -> Product:
        """
        Cria um novo produto.

        Args:
            product: Produto a ser criado

        Returns:
            Product: Produto criado com id atribuído

        Raises:
            sqlite3.IntegrityError: Se código já existe
        """
        conn = self.connection.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO products (name, code, quantity, price, category, description)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                product.name,
                product.code,
                product.quantity,
                product.price,
                product.category,
                product.description,
            ),
        )
        conn.commit()

        product.id = cursor.lastrowid
        product.created_at = datetime.now()
        product.updated_at = datetime.now()

        return product

    def read(self, product_id: int) -> Optional[Product]:
        """
        Recupera um produto por id.

        Args:
            product_id: ID do produto

        Returns:
            Product ou None se não encontrado
        """
        conn = self.connection.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        row = cursor.fetchone()

        return self._row_to_product(row) if row else None

    def read_by_code(self, code: str) -> Optional[Product]:
        """
        Recupera um produto pelo código.

        Args:
            code: Código do produto

        Returns:
            Product ou None se não encontrado
        """
        conn = self.connection.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM products WHERE code = ?", (code,))
        row = cursor.fetchone()

        return self._row_to_product(row) if row else None

    def read_all(self) -> list[Product]:
        """
        Recupera todos os produtos.

        Returns:
            Lista de produtos
        """
        conn = self.connection.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM products ORDER BY name")
        rows = cursor.fetchall()

        return [self._row_to_product(row) for row in rows]

    def search(self, query: str) -> list[Product]:
        """
        Busca produtos por nome ou código.

        Args:
            query: Termo de busca (parcial)

        Returns:
            Lista de produtos encontrados
        """
        conn = self.connection.get_connection()
        cursor = conn.cursor()

        search_term = f"%{query}%"
        cursor.execute(
            """
            SELECT * FROM products
            WHERE name LIKE ? OR code LIKE ?
            ORDER BY name
            """,
            (search_term, search_term),
        )
        rows = cursor.fetchall()

        return [self._row_to_product(row) for row in rows]

    def update(self, product: Product) -> bool:
        """
        Atualiza um produto existente.

        Args:
            product: Produto com dados atualizados

        Returns:
            bool: True se atualizado, False se não encontrado
        """
        if product.id is None:
            raise ValueError("Produto sem id não pode ser atualizado")

        conn = self.connection.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE products
            SET name = ?, quantity = ?, price = ?, category = ?, description = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (
                product.name,
                product.quantity,
                product.price,
                product.category,
                product.description,
                product.id,
            ),
        )
        conn.commit()

        return cursor.rowcount > 0

    def delete(self, product_id: int) -> bool:
        """
        Deleta um produto.

        Args:
            product_id: ID do produto a deletar

        Returns:
            bool: True se deletado, False se não encontrado
        """
        conn = self.connection.get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()

        return cursor.rowcount > 0

    @staticmethod
    def _row_to_product(row: object) -> Product:
        """Converte linha SQLite para objeto Product."""
        return Product(
            id=row["id"],
            name=row["name"],
            code=row["code"],
            quantity=row["quantity"],
            price=row["price"],
            category=row["category"],
            description=row["description"],
            created_at=datetime.fromisoformat(row["created_at"]) if row["created_at"] else None,
            updated_at=datetime.fromisoformat(row["updated_at"]) if row["updated_at"] else None,
        )


class StockMovementRepository:
    """Gerencia operações CRUD para movimentações de estoque."""

    def __init__(self, connection: DatabaseConnection) -> None:
        """
        Inicializa o repositório.

        Args:
            connection: Gerenciador de conexão com banco de dados
        """
        self.connection = connection

    def log_movement(self, movement: StockMovement) -> StockMovement:
        """
        Registra uma movimentação de estoque.

        Args:
            movement: Movimentação a ser registrada

        Returns:
            StockMovement: Movimentação registrada com id atribuído
        """
        conn = self.connection.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO stock_movements (product_id, quantity_change, reason)
            VALUES (?, ?, ?)
            """,
            (movement.product_id, movement.quantity_change, movement.reason),
        )
        conn.commit()

        movement.id = cursor.lastrowid
        movement.timestamp = datetime.now()

        return movement

    def get_movements_by_product(self, product_id: int) -> list[StockMovement]:
        """
        Recupera histórico de movimentações de um produto.

        Args:
            product_id: ID do produto

        Returns:
            Lista de movimentações ordenadas por timestamp (mais recentes primeiro)
        """
        conn = self.connection.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM stock_movements
            WHERE product_id = ?
            ORDER BY timestamp DESC
            """,
            (product_id,),
        )
        rows = cursor.fetchall()

        return [self._row_to_movement(row) for row in rows]

    def get_all_movements(self) -> list[StockMovement]:
        """
        Recupera todas as movimentações.

        Returns:
            Lista de movimentações ordenadas por timestamp (mais recentes primeiro)
        """
        conn = self.connection.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM stock_movements
            ORDER BY timestamp DESC
            """
        )
        rows = cursor.fetchall()

        return [self._row_to_movement(row) for row in rows]

    @staticmethod
    def _row_to_movement(row: object) -> StockMovement:
        """Converte linha SQLite para objeto StockMovement."""
        return StockMovement(
            id=row["id"],
            product_id=row["product_id"],
            quantity_change=row["quantity_change"],
            reason=row["reason"],
            timestamp=datetime.fromisoformat(row["timestamp"]) if row["timestamp"] else datetime.now(),
        )
