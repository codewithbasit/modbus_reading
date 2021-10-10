from app import app
from flask import render_template, redirect, url_for
from app import database as db_helper

@app.route('/')
def index():
    records = db_helper.get_latest_records()
    return render_template('index.html', records=records)

@app.route('/save_record')
def save_record():
    record = db_helper.new_dev_data()
    db_helper.save_record(record)
    return redirect('/', code=302)