from flask import render_template, request, redirect, url_for, Blueprint
import sqlalchemy as db
from sqlalchemy import func
from datetime import datetime
import math
import pandas as pd


# sql setting
path_to_db = "./db/LabPropertyMgt20211231.db"
engine = db.create_engine(f'sqlite:///{path_to_db}',native_datetime=True)
metadata = db.MetaData()
table_PurchasingInfo = db.Table('PurchasingInfo', metadata, autoload=True, autoload_with=engine)
table_PurchasingList = db.Table('PurchasingList', metadata, autoload=True, autoload_with=engine)
table_Member = db.Table('Member', metadata, autoload=True, autoload_with=engine)
table_Supplier = db.Table('Supplier', metadata, autoload=True, autoload_with=engine)

pc_info_app = Blueprint('purchase_info_app', __name__, url_prefix="/pc_info")


@pc_info_app.route('/')
def index(): #show purchasing info
    # query string
    page = int(request.args.get('page') if request.args.get('page') else 1)
    each_page = 30

#     # set total pages
    connection  = engine.connect() # connection 要放在view function中，否則會出現thread error
    query = db.select(func.count()).select_from(table_PurchasingInfo)
    proxy = connection.execute(query)
    total_pages = math.ceil(proxy.fetchall()[0][0]/each_page) # [0][0] => inorder to get the value

    # fetch data & decided by page
    query = db.select(table_PurchasingInfo).limit(each_page).offset((page-1)*each_page)
    proxy = connection.execute(query)
    results = proxy.fetchall()
    #print(results[0].keys())
    print(results)

#     # Close connection
    connection.close()

    return render_template('pc_info.html',
                           page_header="所有提交之採購清單",
                           total_pages=total_pages,
                           outputs=results,
                           page=page)

    #return render_template('index.html',
    #                       page_header="purchase info",
    #                       current_time=datetime.utcnow())

@pc_info_app.route('/info')
def pc_info_show():

    # query string
    page = int(request.args.get('page') if request.args.get('page') else 1)
    each_page = 5

    # set total pages
    connection  = engine.connect() # connection 要放在view function中，否則會出現thread error
    query = db.select(func.count()).select_from(table_PurchasingInfo)
    proxy = connection.execute(query)
    total_pages = math.ceil(proxy.fetchall()[0][0]/each_page) # [0][0] => inorder to get the value

    # fetch data & decided by page
    # query = db.select(table_members).limit(each_page).offset((page-1)*each_page)
    
    query = db.select(table_PurchasingInfo.c.Applicant_ID, table_PurchasingInfo.c.List_ID, table_PurchasingInfo.c.Purchaser_ID).select_from(table_PurchasingInfo).limit(each_page).offset((page-1)*each_page)
    proxy = connection.execute(query)
    sql_results = proxy.fetchall()

    #tmp_df = pd.DataFrame(sql_results, columns=["Applicant_ID",	"List_ID", "SubmitDate", "Purchaser_ID", "AcceptDate", "TransactionDate", "Supplier_ID"])
    tmp_df = pd.DataFrame(sql_results, columns=["Applicant_ID", "List_ID", "Purchaser_ID"])
    results = tmp_df
    print(sql_results)
    print(results)

    #return render_template('index.html',
    #                       page_header="purchase info",
    #                       current_time=datetime.utcnow())
    
    return render_template('pc_info.html',
                           page_header="PurchasingInfo",
                           total_pages=total_pages,
                           outputs=results,
                           page=page)