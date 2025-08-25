#!/usr/bin/env python
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ferreteria_web_project.settings")

import django
django.setup()

from django.core.management import call_command

call_command("migrate")
print("Migraciones aplicadas correctamente.")
