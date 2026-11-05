from src.models.product import Product


def validate_product_name(name: str) -> tuple[bool, str]:
    """
    Valida nome de produto.

    Args:
        name: Nome do produto

    Returns:
        tuple[bool, str]: (é válido, mensagem de erro se houver)
    """
    if not name or not name.strip():
        return False, "Nome do produto não pode estar vazio"

    if len(name) < 3:
        return False, "Nome deve ter no mínimo 3 caracteres"

    if len(name) > 100:
        return False, "Nome não pode ultrapassar 100 caracteres"

    return True, ""


def validate_code(code: str) -> tuple[bool, str]:
    """
    Valida código do produto.

    Args:
        code: Código do produto

    Returns:
        tuple[bool, str]: (é válido, mensagem de erro se houver)
    """
    if not code or not code.strip():
        return False, "Código do produto não pode estar vazio"

    if len(code) < 3:
        return False, "Código deve ter no mínimo 3 caracteres"

    if len(code) > 20:
        return False, "Código não pode ultrapassar 20 caracteres"

    return True, ""


def validate_quantity(quantity: int) -> tuple[bool, str]:
    """
    Valida quantidade de produto.

    Args:
        quantity: Quantidade

    Returns:
        tuple[bool, str]: (é válido, mensagem de erro se houver)
    """
    if not isinstance(quantity, int):
        return False, "Quantidade deve ser um número inteiro"

    if quantity < 0:
        return False, "Quantidade não pode ser negativa"

    return True, ""


def validate_price(price: float) -> tuple[bool, str]:
    """
    Valida preço do produto.

    Args:
        price: Preço do produto

    Returns:
        tuple[bool, str]: (é válido, mensagem de erro se houver)
    """
    if not isinstance(price, (int, float)):
        return False, "Preço deve ser um número"

    if price < 0:
        return False, "Preço não pode ser negativo"

    if price > 999999.99:
        return False, "Preço não pode ser maior que R$ 999999.99"

    return True, ""


def validate_category(category: str) -> tuple[bool, str]:
    """
    Valida categoria do produto.

    Args:
        category: Categoria do produto

    Returns:
        tuple[bool, str]: (é válido, mensagem de erro se houver)
    """
    if not category or not category.strip():
        return False, "Categoria não pode estar vazia"

    if len(category) < 3:
        return False, "Categoria deve ter no mínimo 3 caracteres"

    if len(category) > 50:
        return False, "Categoria não pode ultrapassar 50 caracteres"

    return True, ""


def validate_product(product: Product) -> tuple[bool, list[str]]:
    """
    Valida todos os campos de um produto.

    Args:
        product: Produto a validar

    Returns:
        tuple[bool, list[str]]: (é válido, lista de erros encontrados)
    """
    errors: list[str] = []

    valid, msg = validate_product_name(product.name)
    if not valid:
        errors.append(msg)

    valid, msg = validate_code(product.code)
    if not valid:
        errors.append(msg)

    valid, msg = validate_quantity(product.quantity)
    if not valid:
        errors.append(msg)

    valid, msg = validate_price(product.price)
    if not valid:
        errors.append(msg)

    valid, msg = validate_category(product.category)
    if not valid:
        errors.append(msg)

    return len(errors) == 0, errors
