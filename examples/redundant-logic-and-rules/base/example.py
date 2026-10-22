ALLOWED = frozenset({"tomato", "egg", "salt"})


def describe_dish(ingredients):
    """Accept a tuple of allowed ingredient names; return them joined by ', '."""
    unknown = set(ingredients) - ALLOWED
    if unknown:
        raise ValueError("unsupported ingredients")
    return ", ".join(ingredients)
