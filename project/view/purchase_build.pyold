from flask import render_template, request, redirect, url_for, Blueprint
import sqlalchemy as db
from sqlalchemy import func
from datetime import datetime
import math
import pandas as pd


# sql setting
path_to_db = "./db/LabPropertyMgt20211231.db"

from sqlalchemy.engine import Engine
from sqlalchemy import event

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()




engine = db.create_engine(f'sqlite:///{path_to_db}',native_datetime=True)
metadata = db.MetaData()
table_PurchasingInfo = db.Table('PurchasingInfo', metadata, autoload=True, autoload_with=engine)
table_PurchasingList = db.Table('PurchasingList', metadata, autoload=True, autoload_with=engine)
table_Member = db.Table('Member', metadata, autoload=True, autoload_with=engine)
table_Supplier = db.Table('Supplier', metadata, autoload=True, autoload_with=engine)

pc_build_app = Blueprint('purchase_build_app', __name__, url_prefix="/pc_build")

@pc_build_app.route('/')
def index():
    return render_template('index.html',
                           page_header="purchase build",
                           current_time=datetime.utcnow())


@pc_build_app.route('/Purchasing_submit', methods=["GET", "POST"])
def Purchasing_submit():
    List_ID_GENERATE="None"
    if request.method=="POST":
        try:
            connection  = engine.connect() # connection 要放在view function中，否則會出現thread error
            query = db.select(table_PurchasingList).order_by(table_PurchasingList.c.List_ID)
            proxy = connection.execute(query)
            id_list = [idx[0] for idx in proxy.fetchall()]  

            if request.form['Sn']&request.form['Item']&request.form['Specification']&request.form['Amount']: # 希望至少要填寫名子
                query = db.select(table_PurchasingList.c.List_ID).select_from(table_PurchasingList).order_by(table_PurchasingList.c.List_ID.desc())
                proxy = connection.execute(query)
                List_ID_GENERATE = 'P'+str(int([idx[0] for idx in proxy.fetchall()][0].split('P')[1])+1)        

                query = db.insert(PurchasingInfo).values(Applicant_ID=request.form['Applicant_ID'],List_ID=List_ID_GENERATE,SubmitDate=request.form['Date'],Purchaser_ID=None,AcceptDate=None, TransactionDate=None, DeliveryDate=None, Supplier_ID=None)
                proxy = connection.execute(query)

                query = db.insert(table_PurchasingList).values(List_ID=List_ID_GENERATE,Sn=request.form['Sn'],Item=request.form['Item'],Specification=request.form['Specification'], Amount=request.form['Amount'])
                proxy = connection.execute(query)                

            else:
                raise Exception
        except:
            return render_template('purchasing_submit.html',
                                    page_header="提交採購清單")
        
        finally:
            # Close connection
            connection.close()
           
    if request.method=="GET":
        connection  = engine.connect() # connection 要放在view function中，否則會出現thread error
        query = db.select(table_PurchasingList.c.List_ID).order_by(table_PurchasingList.c.List_ID)
        proxy = connection.execute(query)
        id_list = [idx[0] for idx in proxy.fetchall()]
        connection.close()

        return render_template('purchasing_submit.html',
                                page_header="提交採購清單",id_list=id_list,id_list_property=id_list_property)

