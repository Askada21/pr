class Product:
    def __init__(self, product_id: str):
        self.product_id = product_id

    def __repr__(self):
        return f"Product(product_id={self.product_id!r})"