from src.database.repository import ProductRepository, StockMovementRepository
from src.models.product import Product
from src.models.stock_movement import StockMovement
from src.utils.validators import validate_product


class ProductService:
    """Orquestra operações com produtos e estoque."""

    def __init__(
        self,
        product_repo: ProductRepository,
        movement_repo: StockMovementRepository,
    ) -> None:
        """
        Inicializa o serviço.

        Args:
            product_repo: Repositório de produtos
            movement_repo: Repositório de movimentações
        """
        self.product_repo = product_repo
        self.movement_repo = movement_repo

    def add_product(self, product: Product) -> tuple[bool, str]:
        """
        Adiciona um novo produto ao estoque.

        Args:
            product: Produto a adicionar

        Returns:
            tuple[bool, str]: (sucesso, mensagem)
        """
        valid, errors = validate_product(product)
        if not valid:
            return False, "; ".join(errors)

        try:
            created = self.product_repo.create(product)

            if created.quantity > 0:
                movement = StockMovement(
                    product_id=created.id,
                    quantity_change=created.quantity,
                    reason="Entrada Inicial",
                )
                self.movement_repo.log_movement(movement)

            return True, f"Produto '{product.name}' cadastrado com sucesso"
        except Exception as e:
            return False, f"Erro ao cadastrar produto: {str(e)}"

    def get_product(self, product_id: int) -> Product | None:
        """
        Recupera um produto pelo id.

        Args:
            product_id: ID do produto

        Returns:
            Product ou None se não encontrado
        """
        return self.product_repo.read(product_id)

    def get_all_products(self) -> list[Product]:
        """
        Recupera todos os produtos.

        Returns:
            Lista de produtos
        """
        return self.product_repo.read_all()

    def search_products(self, query: str) -> list[Product]:
        """
        Busca produtos por nome ou código.

        Args:
            query: Termo de busca

        Returns:
            Lista de produtos encontrados
        """
        if not query or not query.strip():
            return self.get_all_products()

        return self.product_repo.search(query.strip())

    def update_product(self, product: Product) -> tuple[bool, str]:
        """
        Atualiza um produto existente.

        Args:
            product: Produto com dados atualizados

        Returns:
            tuple[bool, str]: (sucesso, mensagem)
        """
        if product.id is None:
            return False, "Produto sem id não pode ser atualizado"

        valid, errors = validate_product(product)
        if not valid:
            return False, "; ".join(errors)

        try:
            old_product = self.product_repo.read(product.id)
            if old_product is None:
                return False, "Produto não encontrado"

            updated = self.product_repo.update(product)
            if not updated:
                return False, "Falha ao atualizar produto"

            quantity_diff = product.quantity - old_product.quantity
            if quantity_diff != 0:
                reason = "Entrada" if quantity_diff > 0 else "Saída"
                movement = StockMovement(
                    product_id=product.id,
                    quantity_change=quantity_diff,
                    reason=f"{reason} (Ajuste)",
                )
                self.movement_repo.log_movement(movement)

            return True, f"Produto '{product.name}' atualizado com sucesso"
        except Exception as e:
            return False, f"Erro ao atualizar produto: {str(e)}"

    def delete_product(self, product_id: int) -> tuple[bool, str]:
        """
        Deleta um produto.

        Args:
            product_id: ID do produto a deletar

        Returns:
            tuple[bool, str]: (sucesso, mensagem)
        """
        try:
            product = self.product_repo.read(product_id)
            if product is None:
                return False, "Produto não encontrado"

            deleted = self.product_repo.delete(product_id)
            if not deleted:
                return False, "Falha ao deletar produto"

            return True, f"Produto '{product.name}' removido com sucesso"
        except Exception as e:
            return False, f"Erro ao deletar produto: {str(e)}"

    def adjust_stock(
        self, product_id: int, quantity_change: int, reason: str
    ) -> tuple[bool, str]:
        """
        Ajusta quantidade de estoque de um produto.

        Args:
            product_id: ID do produto
            quantity_change: Quantidade a adicionar/remover
            reason: Motivo do ajuste

        Returns:
            tuple[bool, str]: (sucesso, mensagem)
        """
        if quantity_change == 0:
            return False, "Quantidade de ajuste não pode ser zero"

        if not reason or not reason.strip():
            return False, "Motivo do ajuste é obrigatório"

        try:
            product = self.product_repo.read(product_id)
            if product is None:
                return False, "Produto não encontrado"

            new_quantity = product.quantity + quantity_change
            if new_quantity < 0:
                return False, "Quantidade resultante não pode ser negativa"

            product.quantity = new_quantity
            updated = self.product_repo.update(product)
            if not updated:
                return False, "Falha ao atualizar estoque"

            movement = StockMovement(
                product_id=product_id,
                quantity_change=quantity_change,
                reason=reason,
            )
            self.movement_repo.log_movement(movement)

            return True, f"Estoque de '{product.name}' ajustado com sucesso"
        except Exception as e:
            return False, f"Erro ao ajustar estoque: {str(e)}"

    def get_product_history(self, product_id: int) -> list[StockMovement]:
        """
        Recupera histórico de movimentações de um produto.

        Args:
            product_id: ID do produto

        Returns:
            Lista de movimentações
        """
        return self.movement_repo.get_movements_by_product(product_id)

    def get_all_history(self) -> list[StockMovement]:
        """
        Recupera todas as movimentações.

        Returns:
            Lista de movimentações
        """
        return self.movement_repo.get_all_movements()
