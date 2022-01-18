from flask import render_template, request, redirect, url_for, Blueprint
import sqlalchemy as db
from sqlalchemy import func
from datetime import datetime
import math
from sqlalchemy.engine import Engine
from sqlalchemy import event
import traceback
import sys

# @event.listens_for(Engine, "connect")
# def set_sqlite_pragma(dbapi_connection, connection_record):
#      cursor = dbapi_connection.cursor()
#      cursor.execute("PRAGMA foreign_keys=ON")
#      cursor.close()
    
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
    query = db.select(func.count()).select_from(table_PurchasingList)
    proxy = connection.execute(query)
    total_pages = math.ceil(proxy.fetchall()[0][0]/each_page)

    query = db.select(table_PurchasingList).limit(each_page).offset((page-1)*each_page)
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
            query = db.select(table_PurchasingInfo.c.List_ID).order_by(table_PurchasingInfo.c.List_ID)
            proxy = connection.execute(query)
            id_list = [idx[0] for idx in proxy.fetchall()]

            if request.form['List_ID'] and request.form['Item'] and request.form['Specification'] and request.form['Amount']: 
                query = db.select(table_PurchasingList.c.Sn).select_from(table_PurchasingList).order_by(table_PurchasingList.c.Sn.desc())
                proxy = connection.execute(query)

                sn_list = str(int([idx[0] for idx in proxy.fetchall()][0])+1)
                # print("-------------------------")
                # print(sn_list)
                # print("-------------------------")
                l = 10 - len(sn_list)
                sn_gen = '0' * l
                PurchasingList_SN_GENERATE = sn_gen + sn_list

                query = db.insert(table_PurchasingList).values(List_ID = request.form['List_ID'],Sn=PurchasingList_SN_GENERATE,Item=request.form['Item'],Specification=request.form['Specification'],Amount=request.form['Amount'])
                proxy = connection.execute(query)

            else:
                raise Exception
        except Exception as e:
            error_class = e.__class__.__name__ #取得錯誤類型
            detail = e.args[0] if len(e.args)>=1 else "" #取得詳細內容
            cl, exc, tb = sys.exc_info() #取得Call Stack
            lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
            fileName = lastCallStack[0] #取得發生的檔案名稱
            lineNum = lastCallStack[1] #取得發生的行號
            funcName = lastCallStack[2] #取得發生的函數名稱
            errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
            print(errMsg)
            return render_template('purchasingList_submit.html',
                                    page_header="建立採購物品清單",id_list=id_list,status="Failed",
                                    PurchasingList_SN_GENERATE=PurchasingList_SN_GENERATE)
        else:
            return render_template('purchasingList_submit.html',
                                    page_header="建立採購物品清單",id_list=id_list,status="Success",
                                    PurchasingList_SN_GENERATE=PurchasingList_SN_GENERATE)
        finally:
            connection.close()
           
    if request.method=="GET":
        connection  = engine.connect() 
        query = db.select(table_PurchasingInfo.c.List_ID).order_by(table_PurchasingInfo.c.List_ID)
        proxy = connection.execute(query)
        id_list = [idx[0] for idx in proxy.fetchall()]

        connection.close()

        return render_template('purchasingList_submit.html',page_header="建立採購物品清單",id_list=id_list)

@pc_build_app.route('/pclist_delete', methods=["GET", "POST"])
def purchasing_list_delete():
    if request.method=="POST":
        connection  = engine.connect()
        query = db.select(table_PurchasingList.c.Sn).order_by(table_PurchasingList.c.Sn)
        proxy = connection.execute(query)
        id_list = [idx[0] for idx in proxy.fetchall()]
        try:
            page = int(request.args.get('page') if request.args.get('page') else 1)
            each_page = 30

            sql=db.delete(table_PurchasingList).where(table_PurchasingList.c.Sn==request.form['Sn'])
            proxy = connection.execute(sql)
            connection.close()

        except Exception as e:
            error_class = e.__class__.__name__ #取得錯誤類型
            detail = e.args[0] if len(e.args)>=1 else "" #取得詳細內容
            cl, exc, tb = sys.exc_info() #取得Call Stack
            lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
            fileName = lastCallStack[0] #取得發生的檔案名稱
            lineNum = lastCallStack[1] #取得發生的行號
            funcName = lastCallStack[2] #取得發生的函數名稱
            errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
            print(errMsg)
            return render_template('purchasingList_delete.html',page_header="刪除採購物品清單",status="Failed",id_list=id_list)
        else:
            return render_template('purchasingList_delete.html',page_header="刪除採購物品清單",status="Success",id_list=id_list)
        finally:
            connection.close()

    if request.method=="GET":
        connection  = engine.connect()
        query = db.select(table_PurchasingList.c.Sn).order_by(table_PurchasingList.c.Sn)
        proxy = connection.execute(query)
        id_list = [idx[0] for idx in proxy.fetchall()]
        connection.close()
        
        return render_template('purchasingList_delete.html',page_header="刪除採購物品清單",id_list=id_list)
    