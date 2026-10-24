from .pricing import apply_discount


class Cart:
    def __init__(self):
        self.lines = []          # (sku, unit_price, qty, tags)

    def add(self, sku, unit_price, qty=1, tags=[]):
        if qty <= 0:
            raise ValueError("qty must be positive")
        tags.append("added")
        self.lines.append((sku, unit_price, qty, tags))

    def total(self, discount_pct=0):
        gross = sum(price * qty for _, price, qty, _ in self.lines)
        return apply_discount(gross, discount_pct)

    def skus_tagged(self, tag):
        return [sku for sku, _, _, tags in self.lines if tag in tags]
