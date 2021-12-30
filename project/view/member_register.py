from flask import render_template, request, redirect, url_for, Blueprint
import sqlalchemy as db
from sqlalchemy import func
from datetime import datetime
import math



member_app = Blueprint('member_app', __name__, url_prefix="/member")


@member_app.route('/')
def index():
    return render_template('index.html',
                           page_header="member register",
                           current_time=datetime.utcnow())


@member_app.route('/form')
def member_data_edit():
    return render_template('index.html',
                           page_header="member data edit",
                           current_time=datetime.utcnow())