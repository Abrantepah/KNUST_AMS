# collectstatic.py

import os
from django.core.management import call_command

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ams.settings")
    call_command("collectstatic", interactive=False)
