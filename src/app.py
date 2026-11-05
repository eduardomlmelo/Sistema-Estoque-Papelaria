"""Entry point da aplicação de gerenciamento de estoque."""

from src.database.connection import DatabaseConnection
from src.database.repository import ProductRepository, StockMovementRepository
from src.services.product_service import ProductService
from src.services.report_service import ReportService
from src.gui.main_window import MainWindow
from src.utils.constants import DB_PATH


def main() -> None:
    """Inicia a aplicação."""
    db_connection = DatabaseConnection(DB_PATH)

    product_repo = ProductRepository(db_connection)
    movement_repo = StockMovementRepository(db_connection)

    product_service = ProductService(product_repo, movement_repo)
    report_service = ReportService(product_service)

    app = MainWindow(product_service, report_service)
    app.mainloop()

    db_connection.close()


if __name__ == "__main__":
    main()
