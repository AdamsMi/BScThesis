__author__ = 'dominikmajda'

from source import database_manager

dbManager = database_manager()

row = dbManager.get_connection().cursor()
print row.execute("SELECT COUNT(*) FROM NEWS").fetchone()