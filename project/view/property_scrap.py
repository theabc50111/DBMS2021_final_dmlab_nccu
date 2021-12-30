from flask import render_template, request, redirect, url_for, Blueprint
import sqlalchemy as db
from sqlalchemy import func
from datetime import datetime
import math



pp_scrap_app = Blueprint('property_scrap_app', __name__, url_prefix="/pp_scrap")

@pp_scrap_app.route('/')
def index():
    return render_template('index.html',
                           page_header="property scrap",
                           current_time=datetime.utcnow())

