from app import app
from flask import render_template
from flask_login import login_required
from datetime import datetime, timedelta


import models as models


# Index Admin page
@app.route('/admin')
@login_required
def admin_page():
    return render_template('admin.html')


# Index page
@app.route('/')
def index():
    today = datetime.now().strftime('%Y-%m-%d')
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    rooms = models.Room.query.filter_by(status=models.RoomStatus.AVAILABLE).all()
    return render_template('index.html'
                           , current_time=today
                           , tomorrow=tomorrow
                           , rooms=rooms)