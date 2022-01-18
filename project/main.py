from flask import Flask, render_template, request, redirect, url_for, Blueprint
from flask_moment import Moment
from datetime import datetime
import sqlalchemy as db
from sqlalchemy import func
import math
from view.member_register import member_app
from view.property_info import pp_info_app
from view.property_scrap import pp_scrap_app
from view.property_transfer import pp_trans_app
from view.purchase_build import pc_build_app
from view.purchase_info import pc_info_app
import view.property_info # to avoid circular imports for view.property_info


app = Flask(__name__)
view.property_info.init_app(app) # to avoid circular imports for view.property_info
moment = Moment(app)
app.register_blueprint(member_app)
app.register_blueprint(pp_info_app)
app.register_blueprint(pp_scrap_app)
app.register_blueprint(pp_trans_app)
app.register_blueprint(pc_build_app)
app.register_blueprint(pc_info_app)

@app.route('/')
def index():
    return render_template('index.html',
                           page_header="index",
                           current_time=datetime.utcnow())


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")