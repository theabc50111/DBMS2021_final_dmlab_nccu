from flask import render_template, request, redirect, url_for, Blueprint, flash
from sqlalchemy import func
from datetime import datetime
import math
from flask_sqlalchemy import SQLAlchemy


pp_info_app = Blueprint('property_info_app', __name__, url_prefix="/pp_info")

def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./db/LabPropertyMgt20211231.db'
    db = SQLAlchemy()
    db.init_app(app)
    
    # 財務資料清單
    @pp_info_app.route("/")
    def propertylist():
        properties=db.session.execute("SELECT * FROM Property order by Property_ID")
        return render_template("propertylist.html", books=properties)

    # 登錄財物資料頁面
    @pp_info_app.route("/addproperty")
    def addProperty():   
        item=db.session.execute("SELECT * FROM PurchasingList").fetchall()
        member=db.session.execute("SELECT * FROM Member").fetchall()
        return render_template("addproperty.html", books=item, books2=member)

    # 登錄財物資料 
    @pp_info_app.route("/propertyAdd", methods=["POST"])
    def propertyAdd():
        #當使用者在網頁上點擊 submit 按鈕後，會傳送 POST 方法的 http，我們在 Flask sever 中使用 request.form.get(‘username’) 來接收參數
        property_id=request.form.get("property_id")
        propertyname=request.form.get("propertyname")
        type=request.form.get("type")
        price=request.form.get("price")
        servicelife=request.form.get("servicelife")
        keeper_id=request.form.get("keeper_id")
        startdate=request.form.get("startdate")
        location=request.form.get("location")
        # avoid null values from user's submit
        #if propertyname == '' or type == '' or price == '' or servicelife =='' or keeper_id =='' or startdate == '' or location =='':
        #return render_template('warning.html', message = 'Please fill in all the required information!')
        #else:
        db.session.execute("INSERT INTO Property (Property_ID, PropertyName, Type, Price, ServiceLife, Keeper_ID, StartDate, Location) VALUES (:property_id, :propertyname, :type, :price, :servicelife, :keeper_id, :startdate, :location)",
            {"property_id": property_id, "propertyname": propertyname, "type": type, "price":price,"servicelife":servicelife, "keeper_id":keeper_id, "startdate":startdate, "location":location}) 
        db.session.commit() 
        return redirect(url_for('property_info_app.propertylist'))

    # 財物移轉頁面
    @pp_info_app.route("/transfer/<string:bookid>")
    def propertyTransfer(bookid):
        properties=db.session.execute("SELECT * FROM Property where Property_ID=:book_id",{"book_id":bookid}).fetchall()
        member=db.session.execute("SELECT * FROM Member").fetchall()
        # display data in modify page passing the tuple as parameter in render_template method
        return render_template("transferProperty.html",book=properties , books2=member) 


    # 財物移轉
    @pp_info_app.route("/transfer", methods=["POST"])
    def transfer():
        #store values recieved from HTML form in local variables
        property_id=request.form.get("property_id")
        keeper_id=request.form.get("keeper_id")
        applicant_id=request.form.get("applicant_id")
        propertymanager_id=request.form.get("propertymanager_id")
        today = (datetime.now()).strftime('%Y/%m/%d')    
        db.session.execute("UPDATE Property set Keeper_ID = :keeper, StartDate = :date  where Property_ID=:book_id",{"keeper":str(keeper_id), "date":today, "book_id":str(property_id)})
        db.session.commit()




        
        
        approved = ""
        current_transfer_id=db.session.execute("SELECT max(TransferingList_ID) FROM TransferingInfo ").fetchone()
        current_transfer_id = (current_transfer_id[0]).replace("T", "")
        next_transfer_id = "T" + str(int(current_transfer_id) + 1) 

        # insert 財務移轉資訊
        db.session.execute("INSERT INTO TransferingInfo (TransferingList_ID, Applicant_ID, SubmitDate, Aproved, PropertyManager_ID) VALUES (:transfer_id, :applicant_id, :submitdate, :approved, :propertymanager_id)",
            {"transfer_id": next_transfer_id, "applicant_id": applicant_id, "submitdate":today, "approved":approved, "propertymanager_id": propertymanager_id}) 
        db.session.commit()

        # insert 財務移轉清單
        db.session.execute("INSERT INTO TransferingList (TransferingList_ID, Property_ID, NewKeeper_ID) VALUES (:transfer_id, :property_id, :newkeeper_id)",
        {"transfer_id": next_transfer_id, "property_id": property_id, "newkeeper_id": keeper_id})
        db.session.commit()

        
  
        return redirect(url_for('property_info_app.propertylist'))


    # 財務移轉清單
    @pp_info_app.route("/transferlist")
    def transferList():
        list=db.session.execute("SELECT * FROM TransferingList order by TransferingList_ID")
        return render_template("transferlist.html", books=list)



    # for deleting the 2nd entry, it's like: http://127.0.0.1:5000/bookDelete/2
    @pp_info_app.route("/propertyListDelete/<string:bookid>")
    def propertyListDelete(bookid):
        # create delete query as string
        #strSQL="delete from TransferingList where TransferingList_ID="+str(bookid)
        # execute delete query
        #db.session.execute(strSQL) 
        # commit to database

        db.session.execute("DELETE FROM TransferingList WHERE TransferingList_ID = :keeper",{"keeper":str(bookid)})
        db.session.commit()
        db.session.execute("DELETE FROM TransferingInfo WHERE TransferingList_ID = :keeper",{"keeper":str(bookid)})
        db.session.commit() 
        return redirect(url_for('property_info_app.transferList'))

