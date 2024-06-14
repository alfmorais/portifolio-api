import os
import sys
from typing import Dict

import dj_database_url


class ConnectToDatabase:
    @classmethod
    def handle(cls, development_mode: bool) -> Dict:
        if development_mode is True:
            databases = {
                "default": {
                    "ENGINE": "django.db.backends.postgresql",
                    "NAME": os.environ["DB_NAME"],
                    "USER": os.environ["DB_USERNAME"],
                    "PASSWORD": os.environ["DB_SECRET"],
                    "HOST": os.environ["DB_HOST"],
                    "PORT": os.environ["DB_PORT"],
                }
            }

        condition_to_connect_database = (
            len(sys.argv) > 0 and sys.argv[1] != "collectstatic"
        )

        if condition_to_connect_database:
            database_url = os.getenv("DATABASE_URL", None)

            if database_url is None:
                raise Exception("DATABASE_URL environment variable not defined")

            databases = {"default": dj_database_url.parse(database_url)}

        return databases
