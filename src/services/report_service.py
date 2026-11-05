from datetime import datetime
from pathlib import Path
from typing import Optional
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from src.models.product import Product
from src.services.product_service import ProductService


class ReportService:
    """Gera relatórios de estoque."""

    def __init__(self, product_service: ProductService) -> None:
        """
        Inicializa o serviço.

        Args:
            product_service: Serviço de produtos
        """
        self.product_service = product_service

    def export_inventory_pdf(
        self, output_path: str, category_filter: Optional[str] = None
    ) -> tuple[bool, str]:
        """
        Exporta inventário para PDF.

        Args:
            output_path: Caminho para salvar o PDF
            category_filter: Filtrar por categoria (opcional)

        Returns:
            tuple[bool, str]: (sucesso, mensagem)
        """
        try:
            products = self.product_service.get_all_products()

            if category_filter:
                products = [p for p in products if p.category == category_filter]

            if not products:
                return False, "Nenhum produto encontrado para exportar"

            path = Path(output_path)
            path.parent.mkdir(parents=True, exist_ok=True)

            doc = SimpleDocTemplate(output_path, pagesize=letter)
            elements = []

            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                "CustomTitle",
                parent=styles["Heading1"],
                fontSize=24,
                textColor=colors.HexColor("#1f4788"),
                spaceAfter=12,
                alignment=1,
            )

            title = Paragraph("Relatório de Estoque", title_style)
            elements.append(title)

            date_style = ParagraphStyle(
                "DateStyle",
                parent=styles["Normal"],
                fontSize=10,
                textColor=colors.grey,
                alignment=1,
            )
            date_text = Paragraph(
                f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
                date_style,
            )
            elements.append(date_text)

            if category_filter:
                category_text = Paragraph(
                    f"Categoria: <b>{category_filter}</b>",
                    styles["Normal"],
                )
                elements.append(category_text)

            elements.append(Spacer(1, 0.3 * inch))

            data = [
                [
                    "Código",
                    "Produto",
                    "Categoria",
                    "Quantidade",
                    "Preço Unit.",
                    "Total",
                ]
            ]

            total_value = 0.0
            for product in sorted(products, key=lambda p: p.code):
                item_total = product.quantity * product.price
                total_value += item_total

                data.append(
                    [
                        product.code,
                        product.name,
                        product.category,
                        str(product.quantity),
                        f"R$ {product.price:.2f}",
                        f"R$ {item_total:.2f}",
                    ]
                )

            data.append(
                [
                    "",
                    "",
                    "",
                    "",
                    "<b>TOTAL:</b>",
                    f"<b>R$ {total_value:.2f}</b>",
                ]
            )

            table = Table(data, colWidths=[1.0 * inch, 2.0 * inch, 1.2 * inch, 1.0 * inch, 1.0 * inch, 1.0 * inch])

            table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4788")),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 12),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#e6e6e6")),
                        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                        ("ROWBACKGROUNDS", (0, 1), (-1, -2), [colors.white, colors.HexColor("#f0f0f0")]),
                        ("ALIGN", (3, 0), (-1, -1), "RIGHT"),
                    ]
                )
            )

            elements.append(table)

            doc.build(elements)

            return True, f"Relatório exportado com sucesso: {output_path}"
        except Exception as e:
            return False, f"Erro ao gerar relatório: {str(e)}"

    def get_categories(self) -> list[str]:
        """
        Recupera lista de categorias disponíveis.

        Returns:
            Lista de categorias únicas
        """
        products = self.product_service.get_all_products()
        categories = sorted(set(p.category for p in products))
        return categories

    def get_inventory_summary(self) -> dict[str, object]:
        """
        Gera resumo do inventário.

        Returns:
            Dicionário com estatísticas
        """
        products = self.product_service.get_all_products()

        total_items = sum(p.quantity for p in products)
        total_value = sum(p.quantity * p.price for p in products)
        num_products = len(products)

        by_category = {}
        for product in products:
            if product.category not in by_category:
                by_category[product.category] = {
                    "count": 0,
                    "quantity": 0,
                    "value": 0.0,
                }
            by_category[product.category]["count"] += 1
            by_category[product.category]["quantity"] += product.quantity
            by_category[product.category]["value"] += product.quantity * product.price

        low_stock = [p for p in products if p.quantity < 10]

        return {
            "total_products": num_products,
            "total_items": total_items,
            "total_value": total_value,
            "by_category": by_category,
            "low_stock_products": low_stock,
        }
