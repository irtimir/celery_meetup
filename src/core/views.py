from django.http import HttpResponse

from django.db.migrations.executor import MigrationExecutor
from django.db import connections, DEFAULT_DB_ALIAS


def is_database_synchronized(database: str):
    connection = connections[database]
    connection.prepare_database()
    executor = MigrationExecutor(connection)
    targets = executor.loader.graph.leaf_nodes()
    return not executor.migration_plan(targets)


def healthcheck(request):
    if is_database_synchronized(DEFAULT_DB_ALIAS):
        return HttpResponse('OK')
    else:
        return HttpResponse('NOK', status=400)
