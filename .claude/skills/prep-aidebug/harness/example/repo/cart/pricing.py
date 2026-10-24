def apply_discount(price, pct):
    """Return price reduced by pct percent (0-100), rounded to cents."""
    if not 0 <= pct <= 100:
        raise ValueError("pct must be within 0..100")
    return round(price * (100 - pct) / 100, 2)
