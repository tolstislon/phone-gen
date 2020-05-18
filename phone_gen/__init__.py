from .generator import PhoneNumber

try:
    from .__version__ import version as __version__
except ImportError:  # pragma: no cover
    __version__ = "unknown"

__all__ = ["PhoneNumber", "__version__"]
