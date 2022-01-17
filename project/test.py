import sqlalchemy as db
from sqlalchemy import func
from datetime import datetime
import math
import pandas as pd


from sqlalchemy.engine import Engine
from sqlalchemy import event

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


path_to_db = "./db/sqlite.db"
engine = db.create_engine(f'sqlite:///{path_to_db}')
metadata = db.MetaData()
table_members = db.Table('Member', metadata, autoload=True, autoload_with=engine)
table_ocu = db.Table('Occupation', metadata, autoload=True, autoload_with=engine)

connection  = engine.connect()
query = db.select(table_members,table_ocu.c.Occupation).select_from(table_members.outerjoin(table_ocu))
proxy = connection.execute(query)
results = proxy.fetchall()

print(results)

tmp = pd.DataFrame(results, columns=['ID', 'Name', 'unit', 'Occupation'])
tmp2 = pd.concat([tmp.drop('Occupation', axis=1),pd.get_dummies(tmp['Occupation'])], axis=1)
tmp3 = tmp2.to_dict(orient="records")
print(tmp2)
print(tmp3)
print(tmp3[0].keys())


query = db.insert(table_ocu).values(("ccc","bbb"))
proxy = connection.execute(query)
query = db.select(table_ocu)
proxy = connection.execute(query)
results = proxy.fetchall()

print(results)

