#!/usr/bin/env python3
"""Django administrative utility for lab11."""

import os
import sys


def main() -> None:
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lab11.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Install it with `pip install django`."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
