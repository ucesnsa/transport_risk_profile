import sqlalchemy as db
from sqlalchemy import exc
from utils.db_connection import DBConnection

conn = DBConnection()


def drop_db_table(db_name, tbl_name):
    try:
        print('Dropping table ', db_name + '.' + tbl_name)
        engine = conn.engine
        sql = 'DROP TABLE IF EXISTS ' + str(tbl_name) + ';'
        engine.execute(sql)
        print('table dropped ', db_name + '.' + tbl_name)
    except exc.SQLAlchemyError:
        print('drop_db_table', "Encountered general SQLAlchemyError!")
    except  exc.DataError:
        print('drop_db_table', "Encountered general SQLAlchemyError DataError!")

def write_to_db_table(df, db_name, tbl_name):
    try:
        engine = conn.engine
        df.to_sql(tbl_name, engine, if_exists='append')
        # print ('results table created ', db_name +'.'+tbl_name)
        # print ('count:', len(df))
    except exc.SQLAlchemyError:
        print('write_to_db_table', "Encountered general SQLAlchemyError!")