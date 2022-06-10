from report.db import create_db
from report.conf import settings
import sys


def get_command(command: list = sys.argv[1]):
    """Macros to maange the db"""
    if command == "shell":
        import report.test.shell

    elif command == "migrate":
        create_db(settings.DATABASES["default"]["engine"])

    elif command == "test":
        from report.test import test_db

        test_db.run()

    elif command == "runserver":
        from report.server import runserver

        runserver()


if __name__ == "__main__":
    get_command()
