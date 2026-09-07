"""Detect whether Django REST Framework loads cleanly (Django 6.1 needs DRF 3.18+)."""


def rest_framework_available() -> bool:
    try:
        from rest_framework import generics  # noqa: F401
        return True
    except ImportError:
        return False
