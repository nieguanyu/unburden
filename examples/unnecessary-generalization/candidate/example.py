from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class _RenderOptions:
    punctuation: str
    transport: str = "local"
    cache_backend: str = "none"


class _Renderer(ABC):
    @abstractmethod
    def render(self, name, options):
        raise NotImplementedError


class _PlainRenderer(_Renderer):
    def render(self, name, options):
        return f"Hello, {name}{options.punctuation}"


def _build_renderers():
    return {"plain": _PlainRenderer()}


def render_greeting(name, *, punctuation="!"):
    """Return a plain-text greeting with the caller's punctuation string."""
    options = _RenderOptions(punctuation=punctuation)
    renderers = _build_renderers()
    return renderers["plain"].render(name, options)
