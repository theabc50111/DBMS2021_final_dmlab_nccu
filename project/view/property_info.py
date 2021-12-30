from flask import render_template, request, redirect, url_for, Blueprint
import sqlalchemy as db
from sqlalchemy import func
from datetime import datetime
import math


pp_info_app = Blueprint('property_info_app', __name__, url_prefix="/pp_info")

@pp_info_app.route('/')
def index():
    return render_template('index.html',
                           page_header="property info",
                           current_time=datetime.utcnow())

