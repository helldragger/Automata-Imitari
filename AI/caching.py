import sqlite3
import sys

from AI.config import verbose


db_name: str = "cache.db"
db_path: str = "./cache/"

operations: {
    (str, str, str, str): set
} = {}


def create_table(table_name: str, args: str):
    DB = sqlite3.connect(db_path + db_name)

    c = DB.cursor()
    command = f"CREATE TABLE {table_name} ({args})"
    try:
        c.execute(command)
        print("O)   TABLE " + table_name + " has been created".upper())
    except Exception as e:
        # alreadyExists
        print("X)   TABLE " + table_name + " could not be created:".upper(), e)
    finally:
        c.close()


def prepare_db_tables():
    create_table("operations", "module text, version text, class text, method "
                               "text NOT NULL, var text, type text NOT NULL ")
    create_table("discovered", "module text NOT NULL, version text NOT NULL")


def init_cache():
    print("Building cache")
    # prepare db
    DB = sqlite3.connect(db_path + db_name)
    prepare_db_tables()
    DB.commit()
    DB.close()

    # initialize important variables
    # regen cache
    print("Initializing operations cache data")
    #
    DB = sqlite3.connect(db_path + db_name)
    c = DB.cursor()

    cached = c.execute(f"""
        SELECT module, class, method, var, type
        FROM operations;
        """).fetchall()
    DB.commit()
    DB.close()

    for data in cached:
        if (data[0], data[1], data[2], data[3]) in operations.keys():
            operations[(data[0], data[1], data[2], data[3])].add(data[4])
        else:
            operations[(data[0], data[1], data[2], data[3])] = {data[4]}
        operations[(data[0], data[1], data[2], data[3])].add(data[4])
    print("Initialization done")


def get_operation_from_cache(module: str, version: str, class_: str,
                             method: str, var: str = ""):
    var_condition = ""
    if var != "":
        var_condition = f"""AND var="{var}" """

    DB = sqlite3.connect(db_path + db_name)
    c = DB.cursor()

    results = c.execute(f"""
    SELECT * 
    FROM operations
    WHERE module="{module}" 
    AND class="{class_}"
    AND method="{method}" 
    {var_condition};
    """).fetchall()
    DB.commit()
    DB.close()
    return results


def load_operation_from_cache(module: str, version: str, class_: str,
                              method: str, var: str = "") -> None:
    cached = get_operation_from_cache(module, class_, method, var)
    for data in cached:
        if (data[0], data[1], data[2], data[3]) in operations.keys():
            operations[(data[0], data[1], data[2], data[3])].add(data[4])
        else:
            operations[(data[0], data[1], data[2], data[3])] = {data[4]}
        operations[(data[0], data[1], data[2], data[3])].add(data[4])
    return


def is_operation_cached(module: str, version: str, class_: str,
                        method: str) -> bool:
    return len(get_operation_from_cache(module, version, class_, method)) != 0


def register_operation_into_cache(module: str, version: str, class_: str,
                                  method: str, var: str, type_: str):
    DB = sqlite3.connect(db_path + db_name)
    try:

        c = DB.cursor()

        c.execute(f"""
    INSERT INTO operations (module, version, class , method , var , 
    type) 
    VALUES ("{module}","{version}","{class_}", "{method}", "{var}", "{type_}")
    """)
        if verbose:
            print("Registered new operation: ", module, version, class_, method,
                  var, type_)
    except Exception as e:
        if verbose:
            print(module, version, class_, method, var, type_,
                  "couldn't be added to the "
                  "cache: ", e)
    finally:
        DB.commit()
        DB.close()


def get_installed_module_version(module: str) -> str:
    import pkg_resources
    if module in ["builtins", "sys"]:
        return sys.version
    else:
        return pkg_resources.get_distribution(module).version


def get_cached_module_version(module: str) -> [str]:
    DB = sqlite3.connect(db_path + db_name)
    c = DB.cursor()
    result = c.execute(f"""
                SELECT version 
                FROM discovered
                WHERE module="{module}";
                """).fetchall()
    DB.commit()
    DB.close()
    # unwrap the results in their singletons to a simple list
    result = [v[0] for v in result]
    return result


def is_module_discovered(module: str) -> bool:
    try:
        version = get_installed_module_version(module)
        db_versions = get_cached_module_version(module)
        return version in db_versions
    except Exception as e:
        # unknown module
        return False


def register_discovered_module(module: str, version: str):
    DB = sqlite3.connect(db_path + db_name)
    try:

        c = DB.cursor()

        c.execute(f"""
        INSERT INTO discovered (module, version) 
        VALUES ("{module}","{version}")
        """)
        print("Registered new module: ", module, version)
    except Exception as e:
        print(module, version, "couldn't be added to the "
                               "cache: ", e)
    finally:
        DB.commit()
        DB.close()
