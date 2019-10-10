# This file is part of the Silence framework.
# Silence was developed by the IISSI1-TI team
# (Agustín Borrego, Daniel Ayala, Carlos Ortiz, Inma Hernández & David Ruiz)
# and it is distributed as open source software under the GNU-GPL 3.0 License.

from dal.database.db_connection import get_conn
from dal.DALException import DALException
from pymysql.cursors import DictCursor

from dal.transaction import get_g

# The base Data Access Layer class (implementation for MariaDB/MySQL)
class MariaDBDAL:
    # Query method to retrieve information
    def query(self, q, params=None):
        # Fetch the connection and get a cursor
        conn = get_conn()
        cursor = conn.cursor(DictCursor)
        try:
            # Execute the query, with or without parameters and return the result
            if params:
                cursor.execute(q, params)
            else:
                cursor.execute(q)
            res = cursor.fetchall()
            return res
        except Exception as exc:
            # If anything happens, wrap the exceptions in a DALException
            raise DALException(exc) from exc
        finally:
            # Close the cursor
            cursor.close()

    # Execute method to update information
    def execute(self, q, params=None):
        conn = get_conn()
        cursor = conn.cursor(DictCursor)

        # Check whether we are under autocommit mode or not
        # (it will be false inside a transaction)
        try:
            autocommit = get_g().get("autocommit", True)
        except RuntimeError:
            # Allow this code to run outside the application context
            # (useful for populate_database.py and tests)
            autocommit = True

        # Fetch the connection and get a cursor
        try:
            # Execute the query, with or without parameters and return the result
            if params:
                cursor.execute(q, params)
            else:
                cursor.execute(q)

            # If we're in autocommit mode (true by default), commit the operation
            # This will be false if we're inside a transaction
            if autocommit:
                conn.commit()

            # Return the ID of the row that was modified or inserted
            return cursor.lastrowid
        except Exception as exc:
            # Rollback the operation if we're under autocommit mode and
            # wrap the exception in a DALException
            if autocommit:
                conn.rollback()
            raise DALException(exc) from exc
        finally:
            # Close the cursor
            cursor.close()