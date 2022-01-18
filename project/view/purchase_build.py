from flask import render_template, request, redirect, url_for, Blueprint
import sqlalchemy as db
from sqlalchemy import func
from datetime import datetime
import math
from sqlalchemy.engine import Engine
from sqlalchemy import event

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
    
pc_build_app = Blueprint('purchase_build_app', __name__, url_prefix="/pc_build")

path_to_db = "./db/LabPropertyMgt20211231.db"
table_name_PurchasingInfo = 'PurchasingInfo'
table_name_PurchasingList = 'PurchasingList'
# table_name_Distribution = 'Distribution'
# table_name_BargainingQuotation = 'BargainingQuotation'
engine = db.create_engine(f'sqlite:///{path_to_db}',native_datetime=True)


metadata = db.MetaData()
table_PurchasingInfo = db.Table(table_name_PurchasingInfo, metadata, autoload=True, autoload_with=engine)
table_PurchasingList  = db.Table(table_name_PurchasingList, metadata, autoload=True, autoload_with=engine)


@pc_build_app.route('/')
def index(): #show PurchasingList

    page = int(request.args.get('page') if request.args.get('page') else 1)
    each_page = 30

    connection  = engine.connect() 
    query = db.select(func.count()).select_from(table_PurchasingInfo)
    proxy = connection.execute(query)
    total_pages = math.ceil(proxy.fetchall()[0][0]/each_page)

    query = db.select(table_PurchasingInfo).limit(each_page).offset((page-1)*each_page)
    proxy = connection.execute(query)
    results = proxy.fetchall()
    print(results[0].keys())


    connection.close()
    
    return render_template('PurchasingList_table.html',
                           page_header="所有申請之採購物品清單",
                           total_pages=total_pages,
                           outputs=results,
                           page=page)


@pc_build_app.route('/pclist_submit', methods=["GET", "POST"])
def Purchasing_submit():
    PurchasingList_SN_GENERATE="None"

    if request.method=="POST":
        try:
            connection  = engine.connect() 
            query = db.select(table_PurchasingList.c.List_ID).order_by(table_PurchasingList.c.List_ID)
            proxy = connection.execute(query)
            id_list = [idx[0] for idx in proxy.fetchall()]

            # query = db.select(table_PurchasingList.c.SN).order_by(table_PurchasingList.c.SN)
            # proxy = connection.execute(query)
            # Item_Sn_list = [idx[0] for idx in proxy.fetchall()]
  
            # query = db.select(table_Distribution.c.PurchasedItem_Sn).order_by(table_PurchasingList.c.PurchasedItem_Sn)
            # proxy = connection.execute(query)
            # Item_Sn_list_distr = [idx[0] for idx in proxy.fetchall()]
  
            # query = db.select(table_BargainingQuotation.c.Item_Sn).order_by(table_PurchasingList.c.Item_Sn)
            # proxy = connection.execute(query)
            # Item_Sn_list_bq = [idx[0] for idx in proxy.fetchall()]
  

            if request.form['Item']&request.form['Specification']&request.form['Amount']: 
                query = db.select(table_PurchasingList.c.List_ID).select_from(table_PurchasingList).order_by(table_PurchasingList.c.List_ID.desc())
                proxy = connection.execute(query)
                PurchasingList_SN_GENERATE = 'S'+str(int([idx[0] for idx in proxy.fetchall()][0].split('S')[1])+1)

                query = db.insert(table_PurchasingList).values(SN=PurchasingList_SN_GENERATE,Item=request.form['Item'],Specification=request.form['Specification'],Amount=request.form['Amount'])
                proxy = connection.execute(query)
                # query = db.insert(table_Distribution).values(PurchasedItem_Sn=PurchasingList_SN_GENERATE)
                # proxy = connection.execute(query)
                # query = db.insert(table_BargainingQuotation).values(Item_Sn=PurchasingList_SN_GENERATE)
                # proxy = connection.execute(query)
            else:
                raise Exception
        except:
            return render_template('purchasingList_submit.html',
                                    page_header="建立採購物品清單",id_list=id_list,status="Failed",
                                    PurchasingList_SN_GENERATE=PurchasingList_SN_GENERATE)
                                    #Item_Sn_list=Item_Sn_list,Item_Sn_list_distr=Item_Sn_list_distr,Item_Sn_list_bq=Item_Sn_list_bq,
        else:
            return render_template('purchasingList_submit.html',
                                    page_header="建立採購物品清單",id_list=id_list,status="Success",
                                    PurchasingList_SN_GENERATE=PurchasingList_SN_GENERATE)
                                    #Item_Sn_list=Item_Sn_list,Item_Sn_list_distr=Item_Sn_list_distr,Item_Sn_list_bq=Item_Sn_list_bq,
        finally:
            connection.close()
           
    if request.method=="GET":
        connection  = engine.connect() 
        query = db.select(table_PurchasingList.c.List_ID).order_by(table_PurchasingList.c.List_ID)
        proxy = connection.execute(query)
        id_list = [idx[0] for idx in proxy.fetchall()]
        # query = db.select(table_PurchasingList.c.SN).order_by(table_PurchasingList.c.SN)
        # proxy = connection.execute(query)
        # Item_Sn_list = [idx[0] for idx in proxy.fetchall()]
  
        # query = db.select(table_Distribution.c.PurchasedItem_Sn).order_by(table_PurchasingList.c.PurchasedItem_Sn)
        # proxy = connection.execute(query)
        # Item_Sn_list_distr = [idx[0] for idx in proxy.fetchall()]
  
        # query = db.select(table_BargainingQuotation.c.Item_Sn).order_by(table_PurchasingList.c.Item_Sn)
        # proxy = connection.execute(query)
        # Item_Sn_list_bq = [idx[0] for idx in proxy.fetchall()]

        connection.close()

        return render_template('purchasingList_submit.html',
                                    page_header="建立採購物品清單",id_list=id_list)

