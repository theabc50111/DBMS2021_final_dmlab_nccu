from flask import render_template, request, redirect, url_for, Blueprint
import sqlalchemy as db
from sqlalchemy import func
from datetime import datetime
import math


pc_info_app = Blueprint('purchase_info_app', __name__, url_prefix="/pc_info")

@pc_info_app.route('/')
def index():
    return render_template('index.html',
                           page_header="purchase info",
                           current_time=datetime.utcnow())

