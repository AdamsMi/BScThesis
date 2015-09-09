from source import database_manager

__author__ = 'dominikmajda'

dbManager = database_manager()


dupa = dbManager.get_connection().cursor()
print dupa.execute("SELECT COUNT(*) FROM NEWS").fetchone()