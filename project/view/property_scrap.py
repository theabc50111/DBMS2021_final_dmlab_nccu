from flask import render_template, request, redirect, url_for, Blueprint
import sqlalchemy as db
from sqlalchemy import func
from datetime import datetime
import math



pp_scrap_app = Blueprint('property_scrap_app', __name__, url_prefix="/pp_scrap")

# sql setting
path_to_db = "./db/LabPropertyMgt20211231.db"
table_name_ScrappingInfo = 'ScrappingInfo'
table_name_ScrappingList = 'ScrappingList'
table_name_Property = 'Property'
table_name_Member='Member'
engine = db.create_engine(f'sqlite:///{path_to_db}',native_datetime=True)

# connection  = engine.connect()

metadata = db.MetaData()
table_ScrappingInfo = db.Table(table_name_ScrappingInfo, metadata, autoload=True, autoload_with=engine)
table_ScrappingList  = db.Table(table_name_ScrappingList, metadata, autoload=True, autoload_with=engine)
table_Property  = db.Table(table_name_Property, metadata, autoload=True, autoload_with=engine)
table_Member= db.Table(table_name_Member, metadata, autoload=True, autoload_with=engine)


@pp_scrap_app.route('/')
def index(): #show scrappinginfo
    # query string
    page = int(request.args.get('page') if request.args.get('page') else 1)
    each_page = 30

#     # set total pages
    connection  = engine.connect() # connection 要放在view function中，否則會出現thread error
    query = db.select(func.count()).select_from(table_ScrappingInfo)
    proxy = connection.execute(query)
    total_pages = math.ceil(proxy.fetchall()[0][0]/each_page) # [0][0] => inorder to get the value

    # fetch data & decided by page
    query = db.select(table_ScrappingInfo).limit(each_page).offset((page-1)*each_page)
    proxy = connection.execute(query)
    results = proxy.fetchall()
    print(results[0].keys())

#     # Close connection
    connection.close()
    
    return render_template('scrapping_table.html',
                           page_header="所有提交之報廢清單",
                           total_pages=total_pages,
                           outputs=results,
                           page=page)


@pp_scrap_app.route('/Scrapping_submit', methods=["GET", "POST"])
def Scrapping_submit():
    ScrappingList_ID_GENERATE="None"
    if request.method=="POST":
        try:
            connection  = engine.connect() # connection 要放在view function中，否則會出現thread error
            query = db.select(table_Member.c.Member_ID).order_by(table_Member.c.Member_ID)
            proxy = connection.execute(query)
            id_list = [idx[0] for idx in proxy.fetchall()]
  

            query = db.select(table_Property.c.Property_ID).order_by(table_Property.c.Property_ID)
            proxy = connection.execute(query)
            id_list_property = [idx[0] for idx in proxy.fetchall()]

            if request.form['Applicant_ID']: # 希望至少要填寫名子
                query = db.select(table_ScrappingInfo.c.ScrappingList_ID).select_from(table_ScrappingInfo).order_by(table_ScrappingInfo.c.ScrappingList_ID.desc())
                proxy = connection.execute(query)
                ScrappingList_ID_GENERATE = 'S'+str(int([idx[0] for idx in proxy.fetchall()][0].split('S')[1])+1)
        

                # query = db.insert(table_ScrappingInfo).values(ScrappingList_ID=request.form['ScrappingList_ID'],Applicant_ID=request.form['Applicant_ID'],SubmitDate=request.form['Date'],Reason=request.form['Reason'],PropertyManager_ID=None)
                query = db.insert(table_ScrappingInfo).values(ScrappingList_ID=ScrappingList_ID_GENERATE,Applicant_ID=request.form['Applicant_ID'],SubmitDate=request.form['Date'],Reason=request.form['Reason'],PropertyManager_ID=None)
                proxy = connection.execute(query)
                # query = db.insert(table_ScrappingInfo).values(ScrappingList_ID=request.form['ScrappingList_ID'],Applicant_ID=request.form['Applicant_ID'],SubmitDate=None,Reason=request.form['Reason'])
                # proxy = connection.execute(query)
                query = db.insert(table_ScrappingList).values(ScrappingList_ID=ScrappingList_ID_GENERATE,Property_ID=request.form['Property_ID'])
                proxy = connection.execute(query)
            else:
                raise Exception
        except:
            return render_template('scrapping_submit.html',
                                    page_header="提交報廢需求",id_list=id_list,id_list_property=id_list_property,status="Failed",
                                    ScrappingList_ID_GENERATE=ScrappingList_ID_GENERATE)
        else:
            return render_template('scrapping_submit.html',
                                    page_header="提交報廢需求",id_list=id_list,id_list_property=id_list_property,status="Success",
                                    ScrappingList_ID_GENERATE=ScrappingList_ID_GENERATE)
        finally:
            # Close connection
            connection.close()
           
    if request.method=="GET":
        connection  = engine.connect() # connection 要放在view function中，否則會出現thread error
        query = db.select(table_Member.c.Member_ID).order_by(table_Member.c.Member_ID)
        proxy = connection.execute(query)
        id_list = [idx[0] for idx in proxy.fetchall()]
        connection.close()

        connection  = engine.connect() # connection 要放在view function中，否則會出現thread error
        query = db.select(table_Property.c.Property_ID).order_by(table_Property.c.Property_ID)
        proxy = connection.execute(query)
        id_list_property = [idx[0] for idx in proxy.fetchall()]
        connection.close()

        return render_template('scrapping_submit.html',
                                page_header="提交報廢需求",id_list=id_list,id_list_property=id_list_property)


@pp_scrap_app.route('/Scrapping_aspect', methods=["GET", "POST"])
def Scrapping_aspect():

    if request.method=="POST":
        try:
            connection  = engine.connect() # connection 要放在view function中，否則會出現thread error
            query = db.select(table_Member.c.Member_ID).order_by(table_Member.c.Member_ID)
            proxy = connection.execute(query)
            id_list = [idx[0] for idx in proxy.fetchall()]

            connection  = engine.connect() # connection 要放在view function中，否則會出現thread error
            query = db.select(table_ScrappingInfo.c.ScrappingList_ID).order_by(table_ScrappingInfo.c.ScrappingList_ID)
            proxy = connection.execute(query)
            id_list_Scrapping_list = [idx[0] for idx in proxy.fetchall()]

            

            # 開始處理報廢
            # 新增執行報廢之財務管理人
            # PropertyManager_ID=request.form[PropertyManager_ID]
            query =  db.update(table_ScrappingInfo).where(table_ScrappingInfo.c.ScrappingList_ID ==request.form['ScrappingList_ID'] ).values(PropertyManager_ID=request.form['PropertyManager_ID'])
            # query = db.insert(table_ScrappingInfo).values(ScrappingList_ID=request.form['ScrappingList_ID'],Applicant_ID=request.form['Applicant_ID'],SubmitDate=None,Reason=request.form['Reason'])
            proxy = connection.execute(query)
            # 刪除財物
            # query = db.insert(table_ScrappingInfo).values(ScrappingList_ID=request.form['ScrappingList_ID'],Applicant_ID=request.form['Applicant_ID'],SubmitDate=None,Reason=request.form['Reason'])
            sql=db.text("Delete From Property where Property_ID in (select ScrappingList.Property_ID from ScrappingList where ScrappingList_ID='"+request.form['ScrappingList_ID']+"')")
            # sql=db.delete(table_Property).where(table_Property.c.Property_ID.in_((db.select(table_name_ScrappingList.c.Property_ID).where(table_name_ScrappingList.c.ScrappingList_ID==request.form['ScrappingList_ID']))) )
            proxy = connection.execute(sql)
            print(sql)
            # query = db.insert(table_ScrappingList).values(ScrappingList_ID=request.form['ScrappingList_ID'],Property_ID=request.form['Property_ID'])
            # proxy = connection.execute(query)
  

        except:
            return render_template('scrapping_aspect.html',
                                    page_header="核准報廢清單",id_list=id_list,id_list_Scrapping_list=id_list_Scrapping_list,status="Failed")
        else:
            return render_template('scrapping_aspect.html',
                                    page_header="核准報廢清單",id_list=id_list,id_list_Scrapping_list=id_list_Scrapping_list,status="Success")
        finally:
            # Close connection
            connection.close()

    if request.method=="GET":
        connection  = engine.connect() # connection 要放在view function中，否則會出現thread error
        query = db.select(table_Member.c.Member_ID).order_by(table_Member.c.Member_ID)
        proxy = connection.execute(query)
        id_list = [idx[0] for idx in proxy.fetchall()]
        connection.close()

        connection  = engine.connect() # connection 要放在view function中，否則會出現thread error
        query =  db.select(table_ScrappingInfo.c.ScrappingList_ID).where(table_ScrappingInfo.c.PropertyManager_ID==None).order_by(table_ScrappingInfo.c.ScrappingList_ID)
        proxy = connection.execute(query)
        id_list_Scrapping_list = [idx[0] for idx in proxy.fetchall()]
        connection.close()
        
        return render_template('scrapping_aspect.html',
                                page_header="核准報廢清單",id_list=id_list,id_list_Scrapping_list=id_list_Scrapping_list)
    

@pp_scrap_app.route('/Scrapping_search', methods=["GET", "POST"])
def Scrapping_search():
    if request.method=="POST":
        connection  = engine.connect() # connection 要放在view function中，否則會出現thread error
        query = db.select(table_ScrappingList.c.ScrappingList_ID).order_by(table_ScrappingList.c.ScrappingList_ID)
        proxy = connection.execute(query)
        id_list_Scrapping_list = [idx[0] for idx in proxy.fetchall()]
        try:


            page = int(request.args.get('page') if request.args.get('page') else 1)
            each_page = 30
        
 # set total pages
            query = db.select(func.count()).select_from(table_ScrappingList).where(table_ScrappingList.c.ScrappingList_ID==request.form['ScrappingList_ID'])
            proxy = connection.execute(query)
            total_pages = math.ceil(proxy.fetchall()[0][0]/each_page) # [0][0] => inorder to get the value

            # fetch data & decided by page
            query = db.select(table_ScrappingList).where(table_ScrappingList.c.ScrappingList_ID==request.form['ScrappingList_ID']).limit(each_page).offset((page-1)*each_page)
            # sql=db.select(table_ScrappingList).where(table_ScrappingList.c.ScrappingList_ID==request.form['ScrappingList_ID'],Applicant_ID=request.form['Applicant_ID'] )
            # 
            proxy = connection.execute(query)
            results = proxy.fetchall()
            print(results[0].keys())


            connection.close()

        except:
            return render_template('scrapping_search.html',
                    page_header="查詢報廢清單物品",status="Failed",id_list_Scrapping_list=id_list_Scrapping_list)
        else:
            return render_template('scrapping_search.html',
                    page_header="查詢報廢清單物品",
                    total_pages=total_pages,
                    outputs=results,status="Success")
        finally:
            # Close connection
            connection.close()

    if request.method=="GET":

        connection  = engine.connect() # connection 要放在view function中，否則會出現thread error
        query =  db.select(table_ScrappingInfo.c.ScrappingList_ID).where(table_ScrappingInfo.c.PropertyManager_ID==None).order_by(table_ScrappingInfo.c.ScrappingList_ID)
        proxy = connection.execute(query)
        id_list_Scrapping_list = [idx[0] for idx in proxy.fetchall()]
        connection.close()
        
        return render_template('scrapping_search.html',
                                page_header="查詢報廢清單物品",
                                id_list_Scrapping_list=id_list_Scrapping_list)
    
