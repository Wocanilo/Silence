# This file is part of the Silence framework.
# Silence was developed by the IISSI1-TI team
# (Agustín Borrego, Daniel Ayala, Carlos Ortiz, Inma Hernández & David Ruiz)
# and it is distributed as open source software under the GNU-GPL 3.0 License.

from dal.database.db_connection import get_conn
from dal.DALException import DALException
from pymysql.cursors import DictCursor
from dal.database.db_connection import oracle_engine
from dal.transaction import get_g

# The base Data Access Layer class (implementation for Oracle)
class OracleDAL:
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

            # Return a list of dictionary
            obj = {}
            res = []
            all_data = cursor.fetchall()
            columns = [i[0] for i in cursor.description]

            for data in all_data:
                obj = {}
                for i, col in enumerate(columns):
                    obj[col] = data[i]
                res.append(obj)

            return res
        except Exception as exc:
            # If anything happens, wrap the exceptions in a DALException
            raise DALException(exc) from exc
        finally:
            # Close the cursor
            cursor.close()

    # Get the table name which execute a insert, update, delete query
    def table_name(self, q):
        if q.upper().strip().split(" ")[0] == "INSERT":
            table_name = q.upper().split("INTO")[1].strip().split(" ")[0].strip()

        elif q.upper().strip().split(" ")[0] == "UPDATE":
            table_name = q.upper().strip().split(" ")[1].strip()
        
        else:
            table_name = q.upper().strip().split(" ")[2].strip()
        return table_name            


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
            
            #Return id when insert, update and delete a new element
            #Get the new id
            new_oid = cursor.var(oracle_engine.STRING)
            
            table_name = self.table_name(q)

            oid_query = "SELECT cols.column_name FROM all_constraints cons, all_cons_columns cols WHERE cols.table_name = '"+table_name+"' AND cons.constraint_type = 'P' AND cons.constraint_name = cols.constraint_name AND cons.owner = cols.owner ORDER BY cols.table_name, cols.position"
            oid_name = self.query(oid_query)[0]['COLUMN_NAME']
            q = q + " returning "+oid_name+" into :"+ str(len(params)+1)
            #This transformation is for add a new element
            aux = list(params)
            aux.append(new_oid)
            params = tuple (aux)
            
            # Execute the query, with or without parameters and return the result
            if params:
                cursor.execute(q, params)
            else:
                cursor.execute(q)
            
            oid= new_oid.getvalue()[0]
            # If we're in autocommit mode (true by default), commit the operation
            # This will be false if we're inside a transaction
            if autocommit:
                conn.commit()

            # Return the ID of the row that was modified or inserted
            #return cursor.lastrowid
            
            #cursor.execute("select sec_despacho.currval from DUAL")
            #res = cursor.fetchall()[0][0]
            return oid

        except Exception as exc:
            # Rollback the operation if we're under autocommit mode and
            # wrap the exception in a DALException
            if autocommit:
                conn.rollback()
            raise DALException(exc) from exc
        finally:
            # Close the cursor
            cursor.close()