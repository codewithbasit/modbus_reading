from sqlalchemy.util.langhelpers import counter
from app import app
from flask import json, render_template, redirect, url_for, jsonify, Response
from app import database as db_helper

def json_to_csv(json_data):
    csv = ''
    counter = 0
    if json_data:
        for item in json_data:
            if counter == 0:
                csv += 'Id,Description,Temperature,Humidity,Time\n'
                counter +=1
            else:
                csv += str(item['dev_id'])+','+item['dev_desc']+','+str(item['dev_temp'])+','+str(item['dev_hum'])+','+item['reading_time']+'\n'
    
    return csv

@app.route('/')
def index():
    records = db_helper.get_latest_records()
    return render_template('index.html', records=records)

@app.route('/save_record')
def save_record():
    record = db_helper.new_dev_data()
    db_helper.save_record(record)
    return redirect('/', code=200)

@app.route('/export_csv')
def export_csv():
    records = db_helper.get_all_records()
    response_data = jsonify(records)
    json_data = json.loads((response_data.response[0]))
    csv = json_to_csv(json_data)
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=sensors_data.csv"})
