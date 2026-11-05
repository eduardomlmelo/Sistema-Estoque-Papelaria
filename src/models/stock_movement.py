from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class StockMovement:
    """Representa uma movimentação de estoque (entrada/saída)."""

    product_id: int
    quantity_change: int
    reason: str
    timestamp: datetime = field(default_factory=datetime.now)
    id: Optional[int] = None

    def is_valid(self) -> tuple[bool, str]:
        """
        Valida os dados da movimentação.

        Returns:
            tuple[bool, str]: (é válido, mensagem de erro se houver)
        """
        if self.quantity_change == 0:
            return False, "Quantidade de movimentação não pode ser zero"

        if not self.reason or not self.reason.strip():
            return False, "Motivo da movimentação não pode estar vazio"

        return True, ""

    def __str__(self) -> str:
        sign = "+" if self.quantity_change > 0 else ""
        return f"{sign}{self.quantity_change} ({self.reason}) - {self.timestamp}"
