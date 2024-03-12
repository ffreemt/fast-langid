"""Detect language of text based on fasttext."""
__version__ = "0.1.10"

from .supported_langs import supported_langs
from .fastlid import fastlid

__all__ = (
    "supported_langs",
    "fastlid",
)
