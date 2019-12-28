# This file is part of the Silence framework.
# Silence was developed by the IISSI1-TI team
# (Agustín Borrego, Daniel Ayala, Carlos Ortiz, Inma Hernández & David Ruiz)
# and it is distributed as open source software under the GNU-GPL 3.0 License.

from dal.database.db_connection import get_conn
from dal.database.config import DB_CONFIG

# Method for destroying and creating the database tables
# This shouldn't be modified, it uses the create_database.sql file
def create_database(verbose=False):
    conn = get_conn()
    cursor = conn.cursor()
    
    for script in DB_CONFIG["sql_scripts"]:
        print(f"Executing {script}:")
        with open(f"sql/{script}", "r", encoding="utf-8") as f:
            stmt = ""
            delimiter = ";"
            for line in f:
                if not line or line.strip() == "": continue  # Skip blank lines
                
                # Emulate the DELIMITER sentence
                if "DELIMITER" in line.upper():
                    delimiter = line.split(" ")[1].strip()
                else:
                    if delimiter in line.upper():
                        if delimiter != ";": stmt += line.replace(delimiter, ";")
                        else: stmt += line

                        if verbose: print(stmt)
                        cursor.execute(stmt)
                        stmt = ""
                    else:
                        stmt += line
    conn.commit()
    cursor.close()

#######################################
if __name__ == "__main__":
    print("Creating and populating the database...")
    create_database(verbose=True)
    print("Success!")
