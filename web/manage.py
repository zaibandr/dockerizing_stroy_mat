#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stroy_mat.settings")
    os.environ.setdefault('DJANGO_CONFIGURATION', 'Prod')

    os.environ.setdefault('DB_NAME', 'has_app_db'),
    os.environ.setdefault('DB_USER', 'has_app'),
    os.environ.setdefault('DB_PASS', 'haspswd'),
    os.environ.setdefault('DB_SERVICE', '194.67.215.206'),
    os.environ.setdefault('DB_PORT', '5432')

    from configurations.management import execute_from_command_line

    execute_from_command_line(sys.argv)
