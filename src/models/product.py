from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Product:
    """Representa um produto de papelaria no sistema de estoque."""

    name: str
    code: str
    quantity: int
    price: float
    category: str
    description: str
    id: Optional[int] = None
    created_at: Optional[datetime] = field(default=None)
    updated_at: Optional[datetime] = field(default=None)

    def is_valid(self) -> tuple[bool, str]:
        """
        Valida os dados do produto.

        Returns:
            tuple[bool, str]: (é válido, mensagem de erro se houver)
        """
        if not self.name or not self.name.strip():
            return False, "Nome do produto não pode estar vazio"

        if not self.code or not self.code.strip():
            return False, "Código do produto não pode estar vazio"

        if self.quantity < 0:
            return False, "Quantidade não pode ser negativa"

        if self.price < 0:
            return False, "Preço não pode ser negativo"

        if not self.category or not self.category.strip():
            return False, "Categoria não pode estar vazia"

        return True, ""

    def __str__(self) -> str:
        return f"{self.name} ({self.code}) - R$ {self.price:.2f}"
