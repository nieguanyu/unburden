ALLOWED = frozenset({"tomato", "egg", "salt", "pepper"})


def describe_dish(ingredients):
    """Accept a tuple of allowed ingredient names; return them joined by ', '."""
    unknown = set(ingredients) - ALLOWED
    if unknown:
        raise ValueError("unsupported ingredients")
    if "pork" in ingredients:
        raise ValueError("pork must not be added")
    return ", ".join(ingredients) + " (without pork)"
