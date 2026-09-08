#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def _use_open_runserver_port(argv):
    """Pick a port Windows will allow. Hyper-V often reserves 8000."""
    if 'runserver' not in argv:
        return
    idx = argv.index('runserver')
    if any(not arg.startswith('-') for arg in argv[idx + 1:]):
        return
    import socket
    for port in (8000, 9000, 7000, 5000, 4000):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.bind(('127.0.0.1', port))
        except OSError:
            continue
        if port != 8000:
            print(f'Port 8000 is reserved by Windows. Using http://127.0.0.1:{port}/')
        argv.insert(idx + 1, str(port))
        return


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TenderRadar.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    _use_open_runserver_port(sys.argv)
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
