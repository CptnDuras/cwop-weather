from weather import influx_db


def create_db(db_name):
    db_connection = influx_db.connection
    db_connection.create_database(db_name)
