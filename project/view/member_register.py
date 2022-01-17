from flask import render_template, request, redirect, url_for, Blueprint
import sqlalchemy as db
from sqlalchemy import func
from datetime import datetime
import math
import pandas as pd
from sqlalchemy.engine import Engine
from sqlalchemy import event
import traceback
import sys



@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# sql setting
path_to_db = "./db/LabPropertyMgt20211231.db"
engine = db.create_engine(f'sqlite:///{path_to_db}')
metadata = db.MetaData()
table_members = db.Table('Member', metadata, autoload=True, autoload_with=engine)
table_occupation = db.Table('Occupation', metadata, autoload=True, autoload_with=engine)


member_app = Blueprint('member_app', __name__, url_prefix="/member")


@member_app.route('/')
def index():
    return render_template('index.html',page_header="member functions",current_time=datetime.utcnow())


@member_app.route('/info')
def member_info_show():

    # query string
    page = int(request.args.get('page') if request.args.get('page') else 1)
    each_page = 5

    # set total pages
    connection  = engine.connect() # connection 要放在view function中，否則會出現thread error
    query = db.select(func.count()).select_from(table_members)
    proxy = connection.execute(query)
    total_pages = math.ceil(proxy.fetchall()[0][0]/each_page) # [0][0] => inorder to get the value

    # fetch data & decided by page
    # query = db.select(table_members).limit(each_page).offset((page-1)*each_page)
    query = db.select(table_members,table_occupation.c.Occupation).select_from(table_members.outerjoin(table_occupation)).limit(each_page).offset((page-1)*each_page)
    proxy = connection.execute(query)
    sql_results = proxy.fetchall()

    tmp_df = pd.DataFrame(sql_results, columns=["Member_ID", 'Name', "Unit", "Occupation"])
    results = pd.concat([tmp_df.drop(["Occupation"], axis=1), pd.get_dummies(tmp_df["Occupation"])], axis=1).groupby(["Member_ID", "Name", "Unit"]).sum().astype('bool').reset_index().to_dict(orient="records")
    # print(results)
    # results = pd.concat([tmp_df.drop(["Occupation"], axis=1), pd.get_dummies(tmp_df["Occupation"], dtype='bool')], axis=1).to_dict(orient="records")

    # Close connection
    connection.close()
    
    return render_template('member_info.html',
                           page_header="list members info",
                           total_pages=total_pages,
                           outputs=results,
                           page=page)

@member_app.route('/edit_info', methods=["GET", "POST"])
def member_edit_info():

    if request.method=="POST":
        try:
            connection  = engine.connect() # connection 要放在view function中，否則會出現thread error
            query = db.select(table_members.c.Member_ID).order_by(table_members.c.Member_ID)
            proxy = connection.execute(query)
            id_list = [idx[0] for idx in proxy.fetchall()]
            if request.form['Name'] or request.form['Delete_member']: # 希望至少要填寫名子
                if 'Delete_member' in request.form:
                    query = db.delete(table_members).where(table_members.c.Member_ID == request.form['Member_ID'])
                    connection.execute(query)
                else:
                    query = db.update(table_members).where(table_members.c.Member_ID == request.form['Member_ID']).values(**{k:request.form[k] for k in ['Name', 'Unit']})
                    connection.execute(query)
                    query = db.delete(table_occupation).where(table_occupation.c.Member_ID == request.form['Member_ID'])
                    connection.execute(query)
                    query = db.insert(table_occupation).values([(request.form['Member_ID'], request.form.getlist('Occupation')[i]) for i in range(len(request.form.getlist('Occupation')))])
                    connection.execute(query)
            else:
                raise Exception
        except Exception as e:
            error_class = e.__class__.__name__ #取得錯誤類型
            detail = e.args[0] #取得詳細內容
            cl, exc, tb = sys.exc_info() #取得Call Stack
            lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
            fileName = lastCallStack[0] #取得發生的檔案名稱
            lineNum = lastCallStack[1] #取得發生的行號
            funcName = lastCallStack[2] #取得發生的函數名稱
            errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
            print(errMsg)
            return render_template('member_info_edit.html',
                                    page_header="edit member info",id_list=id_list,status="Failed")
        else:
            return render_template('member_info_edit.html',
                                    page_header="edit member info",id_list=id_list,status="Success")
        finally:
            # Close connection
            connection.close()
           
    if request.method=="GET":
        connection  = engine.connect() # connection 要放在view function中，否則會出現thread error
        query = db.select(table_members.c.Member_ID).order_by(table_members.c.Member_ID)
        proxy = connection.execute(query)
        id_list = [idx[0] for idx in proxy.fetchall()]
        connection.close()
        return render_template('member_info_edit.html',
                                page_header="edit member info",id_list=id_list)


@member_app.route('/register', methods=["GET", "POST"])
def member_register():

    if request.method=="POST":
        try:
            connection  = engine.connect() # connection 要放在view function中，否則會出現thread error
            query = db.select(table_members.c.Member_ID).order_by(table_members.c.Member_ID)
            proxy = connection.execute(query)
            id_list = [idx[0] for idx in proxy.fetchall()]
            if request.form['Name'] and request.form['Member_ID']: # 希望至少要填寫名子
                query = db.insert(table_members).values(**{k:request.form[k] for k in request.form.keys()})
                proxy = connection.execute(query)
            else:
                raise Exception
        except:
            return render_template('member_register.html',
                                    page_header="register",id_list=id_list,status="Failed")
        else:
            return render_template('member_register.html',
                                    page_header="register",id_list=id_list,status="Success")
        finally:
            # Close connection
            connection.close()
           
    if request.method=="GET":
        connection  = engine.connect() # connection 要放在view function中，否則會出現thread error
        query = db.select(table_members.c.Member_ID).order_by(table_members.c.Member_ID)
        proxy = connection.execute(query)
        id_list = [idx[0] for idx in proxy.fetchall()]
        connection.close()
        return render_template('member_register.html',
                                page_header="register",id_list=id_list)

