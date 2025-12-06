from flask import Blueprint, render_template
from helpers.helpers import build_graph

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('index.html')

@views.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@views.route('/settings')
def settings():
    return render_template('settings.html')

@views.route('/governance')
def governance():
    return render_template('governance.html')


# here we can specify number of lines in build_graph function
@views.route('/telemetryTable')
def telemetryTable():
    return render_template('telemetry_table.html', graphs=build_graph())