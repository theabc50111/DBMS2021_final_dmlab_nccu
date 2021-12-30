from flask import render_template, request, redirect, url_for, Blueprint
import sqlalchemy as db
from sqlalchemy import func
from datetime import datetime
import math



pc_build_app = Blueprint('purchase_build_app', __name__, url_prefix="/pc_build")

@pc_build_app.route('/')
def index():
    return render_template('index.html',
                           page_header="purchase build",
                           current_time=datetime.utcnow())

