# This file is part of the Silence framework.
# Silence was developed by the IISSI1-TI team
# (Agustín Borrego, Daniel Ayala, Carlos Ortiz, Inma Hernández & David Ruiz)
# and it is distributed as open source software under the GNU-GPL 3.0 License.

from dal.database.config import DB_CONFIG

try:
    import cx_Oracle as oracle_engine
except ModuleNotFoundError: pass

try:
    import pymysql as mariadb_engine
except ModuleNotFoundError: pass

selected_engine = DB_CONFIG["db_engine"]

# Select the connection that is appropriate for the selected database
# If the selected database is not supported, raise an error.
if selected_engine == "oracle":
    conn = oracle_engine.connect(f'{DB_CONFIG["user"]}/{DB_CONFIG["password"]}@localhost/XE')
elif selected_engine == "mariadb":
    conn = mariadb_engine.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"]
    )
else:
    raise SystemError('DB engine "' + DB_CONFIG["db_engine"] + '" is not supported.')

###############################################################################

def get_conn():
    # Remember to close the cursors!
    return conn
