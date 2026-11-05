import sqlite3
from pathlib import Path
from typing import Optional
from src.database.migrations import SCHEMA_SQL


class DatabaseConnection:
    """Gerencia conexão com banco de dados SQLite."""

    def __init__(self, db_path: str = "data/estoque.db") -> None:
        """
        Inicializa a conexão com banco de dados.

        Args:
            db_path: Caminho para arquivo SQLite
        """
        self.db_path = db_path
        self._connection: Optional[sqlite3.Connection] = None
        self._ensure_directory()

    def _ensure_directory(self) -> None:
        """Cria diretório de dados se não existir."""
        path = Path(self.db_path)
        path.parent.mkdir(parents=True, exist_ok=True)

    def get_connection(self) -> sqlite3.Connection:
        """
        Obtém conexão com banco de dados (cria se não existir).

        Returns:
            sqlite3.Connection: Conexão ativa com banco de dados
        """
        if self._connection is None:
            self._connection = sqlite3.connect(self.db_path)
            self._connection.row_factory = sqlite3.Row
            self.initialize_schema()
        return self._connection

    def initialize_schema(self) -> None:
        """Inicializa schema do banco de dados se necessário."""
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.executescript(SCHEMA_SQL)
        connection.commit()

    def close(self) -> None:
        """Fecha conexão com banco de dados."""
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def __enter__(self) -> "DatabaseConnection":
        """Context manager entry."""
        return self

    def __exit__(self, *args: object) -> None:
        """Context manager exit."""
        self.close()
