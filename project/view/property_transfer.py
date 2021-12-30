from flask import render_template, request, redirect, url_for, Blueprint
import sqlalchemy as db
from sqlalchemy import func
from datetime import datetime
import math


pp_trans_app = Blueprint('property_transfer_app', __name__, url_prefix="/pp_trans")


@pp_trans_app.route('/')
def index():
    return render_template('index.html',
                           page_header="property transfer",
                           current_time=datetime.utcnow())
