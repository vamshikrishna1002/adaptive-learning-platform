def generate_id(prefix: str, number: int) -> str:
    """
    Generate IDs like:
    LRN-000001
    CRS-000001
    SKL-000001
    """

    return f"{prefix}-{number:06d}"