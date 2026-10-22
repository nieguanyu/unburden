def render_greeting(name, *, punctuation="!"):
    """Return a plain-text greeting with the caller's punctuation string."""
    return f"Hello, {name}{punctuation}"
