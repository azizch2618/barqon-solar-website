import logging

from django.db.backends.signals import connection_created

logger = logging.getLogger("barqon")


def configure_sqlite_connection(sender, connection, **kwargs):
    if connection.vendor != "sqlite":
        return

    try:
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA busy_timeout = 30000;")
            cursor.execute("PRAGMA journal_mode = WAL;")
            cursor.execute("PRAGMA synchronous = NORMAL;")
            cursor.execute("PRAGMA temp_store = MEMORY;")
            cursor.execute("PRAGMA foreign_keys = ON;")
    except Exception:
        logger.exception("Unable to apply SQLite stability pragmas.")


connection_created.connect(configure_sqlite_connection)
