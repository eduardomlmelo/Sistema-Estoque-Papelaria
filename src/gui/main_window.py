import tkinter as tk
from tkinter import ttk, messagebox
from src.services.product_service import ProductService
from src.services.report_service import ReportService
from src.models.product import Product
from src.gui.dialogs import ProductDialog, HistoryDialog, ReportDialog
from src.utils.constants import APP_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT


class MainWindow(tk.Tk):
    """Janela principal da aplicação."""

    def __init__(
        self,
        product_service: ProductService,
        report_service: ReportService,
    ) -> None:
        """
        Inicializa a janela principal.

        Args:
            product_service: Serviço de produtos
            report_service: Serviço de relatórios
        """
        super().__init__()
        self.product_service = product_service
        self.report_service = report_service

        self.title(APP_TITLE)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        self._create_widgets()
        self._load_products()

    def _create_widgets(self) -> None:
        """Cria widgets da interface."""
        top_frame = ttk.Frame(self)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        ttk.Label(top_frame, text="Buscar:", font=("Arial", 10)).pack(
            side=tk.LEFT, padx=5
        )

        self.search_var = tk.StringVar()
        self.search_var.trace("w", self._on_search_change)
        search_entry = ttk.Entry(top_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)

        button_frame = ttk.Frame(self)
        button_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        ttk.Button(button_frame, text="Novo Produto", command=self._on_add_product).pack(
            side=tk.LEFT, padx=5
        )

        ttk.Button(button_frame, text="Editar", command=self._on_edit_product).pack(
            side=tk.LEFT, padx=5
        )

        ttk.Button(button_frame, text="Remover", command=self._on_delete_product).pack(
            side=tk.LEFT, padx=5
        )

        ttk.Button(button_frame, text="Histórico", command=self._on_show_history).pack(
            side=tk.LEFT, padx=5
        )

        ttk.Button(button_frame, text="Relatório PDF", command=self._on_generate_report).pack(
            side=tk.LEFT, padx=5
        )

        table_frame = ttk.Frame(self)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columns = ("Código", "Produto", "Qtd", "Preço Unit.", "Total", "Categoria")
        self.tree = ttk.Treeview(table_frame, columns=columns, height=20, show="headings")

        self.tree.column("Código", width=80)
        self.tree.column("Produto", width=250)
        self.tree.column("Qtd", width=60)
        self.tree.column("Preço Unit.", width=90)
        self.tree.column("Total", width=90)
        self.tree.column("Categoria", width=100)

        for col in columns:
            self.tree.heading(col, text=col)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscroll=scrollbar.set)

        status_frame = ttk.Frame(self)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

        self.status_var = tk.StringVar(value="Pronto")
        ttk.Label(
            status_frame,
            textvariable=self.status_var,
            font=("Arial", 9),
            foreground="gray",
        ).pack(anchor=tk.W)

    def _load_products(self) -> None:
        """Carrega todos os produtos na tabela."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        products = self.product_service.get_all_products()
        total_value = 0.0

        for product in sorted(products, key=lambda p: p.name):
            item_total = product.quantity * product.price
            total_value += item_total

            self.tree.insert(
                "",
                tk.END,
                values=(
                    product.code,
                    product.name,
                    product.quantity,
                    f"R$ {product.price:.2f}",
                    f"R$ {item_total:.2f}",
                    product.category,
                ),
                tags=(product.id,),
            )

        self.status_var.set(
            f"Total: {len(products)} produtos | Valor total: R$ {total_value:.2f}"
        )

    def _on_search_change(self, *args: object) -> None:
        """Atualiza tabela ao mudar texto de busca (tempo real)."""
        search_term = self.search_var.get()

        for item in self.tree.get_children():
            self.tree.delete(item)

        if search_term:
            products = self.product_service.search_products(search_term)
        else:
            products = self.product_service.get_all_products()

        for product in sorted(products, key=lambda p: p.name):
            item_total = product.quantity * product.price

            self.tree.insert(
                "",
                tk.END,
                values=(
                    product.code,
                    product.name,
                    product.quantity,
                    f"R$ {product.price:.2f}",
                    f"R$ {item_total:.2f}",
                    product.category,
                ),
                tags=(product.id,),
            )

    def _get_selected_product(self) -> Product | None:
        """Recupera produto selecionado na tabela."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Atenção", "Selecione um produto")
            return None

        item_id = selection[0]
        values = self.tree.item(item_id, "values")
        product_id = int(self.tree.item(item_id, "tags")[0])

        return self.product_service.get_product(product_id)

    def _on_add_product(self) -> None:
        """Adiciona novo produto."""
        dialog = ProductDialog(self)
        product = dialog.get_product()

        if product:
            success, msg = self.product_service.add_product(product)
            if success:
                messagebox.showinfo("Sucesso", msg)
                self._load_products()
            else:
                messagebox.showerror("Erro", msg)

    def _on_edit_product(self) -> None:
        """Edita produto selecionado."""
        product = self._get_selected_product()
        if not product:
            return

        dialog = ProductDialog(self, product)
        updated_product = dialog.get_product()

        if updated_product:
            success, msg = self.product_service.update_product(updated_product)
            if success:
                messagebox.showinfo("Sucesso", msg)
                self._load_products()
            else:
                messagebox.showerror("Erro", msg)

    def _on_delete_product(self) -> None:
        """Deleta produto selecionado."""
        product = self._get_selected_product()
        if not product:
            return

        if messagebox.askyesno(
            "Confirmar",
            f"Deseja remover '{product.name}'?",
        ):
            success, msg = self.product_service.delete_product(product.id)
            if success:
                messagebox.showinfo("Sucesso", msg)
                self._load_products()
            else:
                messagebox.showerror("Erro", msg)

    def _on_show_history(self) -> None:
        """Mostra histórico de movimentações do produto selecionado."""
        product = self._get_selected_product()
        if not product:
            return

        movements = self.product_service.get_product_history(product.id)
        HistoryDialog(self, product.name, movements)

    def _on_generate_report(self) -> None:
        """Abre diálogo para gerar relatório."""
        categories = self.report_service.get_categories()

        def on_generate(path: str, category: str | None) -> None:
            success, msg = self.report_service.export_inventory_pdf(path, category)
            if success:
                messagebox.showinfo("Sucesso", msg)
            else:
                messagebox.showerror("Erro", msg)

        ReportDialog(self, categories, on_generate)
