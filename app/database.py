import sqlite3


def database_init():
    with sqlite3.connect('schedule.db') as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS hosts (id INTEGER PRIMARY KEY AUTOINCREMENT, hostname TEXT NOT NULL)")
        conn.execute("CREATE TABLE IF NOT EXISTS djs (id INTEGER PRIMARY KEY AUTOINCREMENT, djname TEXT NOT NULL)")
        conn.execute("CREATE TABLE IF NOT EXISTS cohosts (id INTEGER PRIMARY KEY AUTOINCREMENT, cohostname TEXT NOT NULL)")
        conn.execute("CREATE TABLE IF NOT EXISTS schedule (id INTEGER PRIMARY KEY AUTOINCREMENT, schedule TEXT NOT NULL)")


def get_db_connection():
    return sqlite3.connect('schedule.db')


def add_record(table, name_column, name):
    with get_db_connection() as conn:
        conn.execute(f"INSERT INTO {table} ({name_column}) VALUES (?)", (name,))


def get_schedule():
    with get_db_connection() as conn:
        record = conn.execute("SELECT schedule FROM schedule LIMIT 1").fetchone()
        return record[0] if record and record[0] else None

def get_records(table, name_column):
    with get_db_connection() as conn:
        records = conn.execute(f"SELECT {name_column} FROM {table}").fetchall()
        return [record[0] for record in records]


def delete_schedule():
    with get_db_connection() as conn:
        conn.execute("DELETE FROM schedule")


def delete_record(table, name_column, name):
    with get_db_connection() as conn:
        conn.execute(f"DELETE FROM {table} WHERE {name_column} = ?", (name,))


def clear_all():
    with get_db_connection() as conn:
        conn.execute("DELETE FROM schedule")
        conn.execute("DELETE FROM hosts")
        conn.execute("DELETE FROM djs")
        conn.execute("DELETE FROM cohosts")


def add_host(name):
    add_record('hosts', 'hostname', name)


def get_hosts():
    return get_records('hosts', 'hostname')


def delete_host(name):
    delete_record('hosts', 'hostname', name)


def add_dj(name):
    add_record('djs', 'djname', name)


def get_djs():
    return get_records('djs', 'djname')


def delete_dj(name):
    delete_record('djs', 'djname', name)


def add_cohost(name):
    add_record('cohosts', 'cohostname', name)


def get_cohosts():
    return get_records('cohosts', 'cohostname')


def delete_cohost(name):
    delete_record('cohosts', 'cohostname', name)
