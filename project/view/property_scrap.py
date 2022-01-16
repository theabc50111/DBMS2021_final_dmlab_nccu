from flask import render_template, request, redirect, url_for, Blueprint
import sqlalchemy as db
from sqlalchemy import func
from datetime import datetime
import math



pp_scrap_app = Blueprint('property_scrap_app', __name__, url_prefix="/pp_scrap")

# sql setting
path_to_db = "./db/LabPropertyMgt20211231.db"
table_ScrappingInfo = 'ScrappingInfo'
table_ScrappingList = 'ScrappingList'
engine = db.create_engine(f'sqlite:///{path_to_db}')
metadata = db.MetaData()
# table_customers = db.Table(table, metadata, autoload=True, autoload_with=engine)


@pp_scrap_app.route('/')
def index():
    return render_template('index.html',
                           page_header="property scrap",
                           current_time=datetime.utcnow())


