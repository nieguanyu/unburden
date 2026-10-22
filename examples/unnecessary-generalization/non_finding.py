from html import escape


def _plain(name, punctuation):
    return f"Hello, {name}{punctuation}"


def _html(name, punctuation):
    return f"<p>Hello, {escape(name)}{escape(punctuation)}</p>"


_RENDERERS = {"plain": _plain, "html": _html}


def render_greeting(name, *, punctuation="!", output_format="plain"):
    """Render a string name and punctuation as caller-selected plain or HTML.

    Raise ValueError for an unsupported output format.
    """
    if output_format not in _RENDERERS:
        raise ValueError("unsupported output format")
    return _RENDERERS[output_format](name, punctuation)
