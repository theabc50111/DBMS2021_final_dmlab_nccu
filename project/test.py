import sqlalchemy as db
from sqlalchemy import func
from datetime import datetime
import math
import pandas as pd


path_to_db = "./db/LabPropertyMgt20211231.db"
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


