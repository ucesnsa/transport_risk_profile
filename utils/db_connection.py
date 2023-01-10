import sqlalchemy as db
from sqlalchemy import exc


class DBConnection(object):
    connection = None
    engine = None

    def __init__(self):
        if DBConnection.connection is None:
            try:
                db_name = 'Roberto_RiskProfile_Oyster'
                engine = db.create_engine('postgresql+psycopg2://postgres:20081979@localhost/' + db_name)
                self.engine = engine
                self.connection = engine.connect()
            except Exception as error:
                print("Error: Connection not established {}".format(error))
            else:
                print("Connection established")

