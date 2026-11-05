import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional
from datetime import datetime
from src.models.product import Product
from src.models.stock_movement import StockMovement
from src.utils.constants import CATEGORIES, MOVEMENT_REASONS


class ProductDialog(tk.Toplevel):
    """Diálogo para adicionar/editar produto."""

    def __init__(self, parent: tk.Widget, product: Optional[Product] = None) -> None:
        """
        Inicializa o diálogo.

        Args:
            parent: Janela pai
            product: Produto a editar (None para novo)
        """
        super().__init__(parent)
        self.product = product
        self.title("Novo Produto" if product is None else "Editar Produto")
        self.geometry("400x500")
        self.resizable(False, False)

        self._create_widgets()

        if product:
            self._load_product_data()

        self.transient(parent)
        self.grab_set()
        self.wait_window()

    def _create_widgets(self) -> None:
        """Cria widgets do formulário."""
        frame = ttk.Frame(self, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Nome:", font=("Arial", 10)).grid(row=0, sticky=tk.W)
        self.name_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.name_var, width=30).grid(
            row=0, column=1, sticky=tk.EW, pady=5
        )

        ttk.Label(frame, text="Código:", font=("Arial", 10)).grid(row=1, sticky=tk.W)
        self.code_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.code_var, width=30).grid(
            row=1, column=1, sticky=tk.EW, pady=5
        )

        ttk.Label(frame, text="Quantidade:", font=("Arial", 10)).grid(row=2, sticky=tk.W)
        self.quantity_var = tk.StringVar(value="0")
        ttk.Spinbox(
            frame,
            from_=0,
            to=999999,
            textvariable=self.quantity_var,
            width=27,
        ).grid(row=2, column=1, sticky=tk.EW, pady=5)

        ttk.Label(frame, text="Preço (R$):", font=("Arial", 10)).grid(row=3, sticky=tk.W)
        self.price_var = tk.StringVar(value="0.00")
        ttk.Entry(frame, textvariable=self.price_var, width=30).grid(
            row=3, column=1, sticky=tk.EW, pady=5
        )

        ttk.Label(frame, text="Categoria:", font=("Arial", 10)).grid(row=4, sticky=tk.W)
        self.category_var = tk.StringVar()
        ttk.Combobox(
            frame,
            textvariable=self.category_var,
            values=CATEGORIES,
            width=27,
            state="readonly",
        ).grid(row=4, column=1, sticky=tk.EW, pady=5)

        ttk.Label(frame, text="Descrição:", font=("Arial", 10)).grid(row=5, sticky=tk.W)
        self.description_var = tk.StringVar()
        text_widget = tk.Text(frame, width=32, height=4)
        text_widget.grid(row=5, column=1, sticky=tk.EW, pady=5)
        self.description_widget = text_widget

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=6, column=0, columnspan=2, sticky=tk.EW, pady=20)

        ttk.Button(button_frame, text="Salvar", command=self._on_save).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(button_frame, text="Cancelar", command=self.destroy).pack(
            side=tk.LEFT, padx=5
        )

        frame.columnconfigure(1, weight=1)

    def _load_product_data(self) -> None:
        """Carrega dados do produto nos campos."""
        if self.product:
            self.name_var.set(self.product.name)
            self.code_var.set(self.product.code)
            self.quantity_var.set(str(self.product.quantity))
            self.price_var.set(f"{self.product.price:.2f}")
            self.category_var.set(self.product.category)
            self.description_widget.insert("1.0", self.product.description or "")

    def _on_save(self) -> None:
        """Salva o produto."""
        try:
            quantity = int(self.quantity_var.get())
            price = float(self.price_var.get())

            if self.product:
                self.product.name = self.name_var.get()
                self.product.quantity = quantity
                self.product.price = price
                self.product.category = self.category_var.get()
                self.product.description = self.description_widget.get("1.0", tk.END).strip()
            else:
                self.product = Product(
                    name=self.name_var.get(),
                    code=self.code_var.get(),
                    quantity=quantity,
                    price=price,
                    category=self.category_var.get(),
                    description=self.description_widget.get("1.0", tk.END).strip(),
                )

            self.destroy()
        except ValueError:
            messagebox.showerror("Erro", "Quantidade e preço devem ser números válidos")

    def get_product(self) -> Optional[Product]:
        """Retorna o produto editado."""
        return self.product


class HistoryDialog(tk.Toplevel):
    """Diálogo para visualizar histórico de movimentações."""

    def __init__(
        self,
        parent: tk.Widget,
        product_name: str,
        movements: list[StockMovement],
    ) -> None:
        """
        Inicializa o diálogo.

        Args:
            parent: Janela pai
            product_name: Nome do produto
            movements: Lista de movimentações
        """
        super().__init__(parent)
        self.title(f"Histórico - {product_name}")
        self.geometry("600x400")

        title = ttk.Label(
            self,
            text=f"Histórico de Movimentações: {product_name}",
            font=("Arial", 12, "bold"),
        )
        title.pack(pady=10)

        frame = ttk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columns = ("Quantid.", "Motivo", "Data")
        self.tree = ttk.Treeview(frame, columns=columns, height=15, show="headings")

        self.tree.column("Quantid.", width=80)
        self.tree.column("Motivo", width=200)
        self.tree.column("Data", width=200)

        for col in columns:
            self.tree.heading(col, text=col)

        for movement in sorted(movements, key=lambda m: m.timestamp, reverse=True):
            quantity_str = f"+{movement.quantity_change}" if movement.quantity_change > 0 else str(movement.quantity_change)
            timestamp_str = movement.timestamp.strftime("%d/%m/%Y %H:%M:%S")
            self.tree.insert(
                "",
                tk.END,
                values=(quantity_str, movement.reason, timestamp_str),
            )

        self.tree.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscroll=scrollbar.set)

        ttk.Button(self, text="Fechar", command=self.destroy).pack(pady=10)

        self.transient(parent)
        self.grab_set()


class ReportDialog(tk.Toplevel):
    """Diálogo para gerar relatórios."""

    def __init__(
        self,
        parent: tk.Widget,
        categories: list[str],
        on_generate: object,
    ) -> None:
        """
        Inicializa o diálogo.

        Args:
            parent: Janela pai
            categories: Lista de categorias disponíveis
            on_generate: Callback para gerar relatório
        """
        super().__init__(parent)
        self.title("Gerar Relatório")
        self.geometry("400x250")
        self.resizable(False, False)
        self.on_generate = on_generate

        frame = ttk.Frame(self, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Tipo de Relatório:", font=("Arial", 10)).pack(anchor=tk.W)

        self.report_type_var = tk.StringVar(value="todos")
        ttk.Radiobutton(
            frame,
            text="Todos os produtos",
            variable=self.report_type_var,
            value="todos",
            command=self._on_report_type_changed,
        ).pack(anchor=tk.W, pady=5)

        ttk.Radiobutton(
            frame,
            text="Por categoria",
            variable=self.report_type_var,
            value="categoria",
            command=self._on_report_type_changed,
        ).pack(anchor=tk.W, pady=5)

        ttk.Label(frame, text="Categoria:", font=("Arial", 10)).pack(anchor=tk.W, pady=(10, 0))
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(
            frame,
            textvariable=self.category_var,
            values=categories,
            state="disabled",
        )
        self.category_combo.pack(anchor=tk.W, fill=tk.X, pady=5)

        ttk.Label(frame, text="Destino:", font=("Arial", 10)).pack(anchor=tk.W, pady=(10, 0))

        path_frame = ttk.Frame(frame)
        path_frame.pack(anchor=tk.W, fill=tk.X, pady=5)

        self.path_var = tk.StringVar(value="relatorios/estoque.pdf")
        ttk.Entry(path_frame, textvariable=self.path_var).pack(
            side=tk.LEFT, fill=tk.X, expand=True
        )

        ttk.Button(
            path_frame,
            text="...",
            width=3,
            command=self._on_browse_path,
        ).pack(side=tk.LEFT, padx=5)

        button_frame = ttk.Frame(frame)
        button_frame.pack(anchor=tk.E, pady=20)

        ttk.Button(button_frame, text="Gerar", command=self._on_generate).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(button_frame, text="Cancelar", command=self.destroy).pack(
            side=tk.LEFT, padx=5
        )

        self.transient(parent)
        self.grab_set()

    def _on_report_type_changed(self) -> None:
        """Atualiza estado dos controles ao mudar tipo de relatório."""
        if self.report_type_var.get() == "categoria":
            self.category_combo.configure(state="readonly")
        else:
            self.category_combo.configure(state="disabled")

    def _on_browse_path(self) -> None:
        """Abre diálogo para escolher caminho do arquivo."""
        path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
        )
        if path:
            self.path_var.set(path)

    def _on_generate(self) -> None:
        """Gera o relatório."""
        report_type = self.report_type_var.get()
        path = self.path_var.get()

        category = None
        if report_type == "categoria":
            category = self.category_var.get()
            if not category:
                messagebox.showerror("Erro", "Selecione uma categoria")
                return

        self.on_generate(path, category)
        self.destroy()
