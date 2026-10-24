def page(items, page_no, size):
    """Return the items on 1-indexed page `page_no`."""
    if page_no < 1 or size < 1:
        raise ValueError("page_no and size must be >= 1")
    start = (page_no - 1) * size
    return items[start:start + size]
