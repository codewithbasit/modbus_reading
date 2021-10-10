from flask import Flask, app, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from datetime import datetime
import os

db_dir = 'data/'
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, 'sensors.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =  False

db =  SQLAlchemy(app)

class DeviceData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dev_id = db.Column(db.Integer)
    dev_desc = db.Column(db.String(255))
    dev_temp = db.Column(db.Float)
    dev_hum = db.Column(db.Float)
    reading_time = db.Column(db.DateTime(timezone=True), nullable=False)

def new_dev_data():
    new_data = DeviceData(
        dev_id = 41,
        dev_desc = "Outdoor sensor",
        dev_temp = 21.3,
        dev_hum = 48.5,
        reading_time=datetime.now()
    )
    
    return new_data

@app.route('/')
def index():
    # new_rec= new_dev_data()
    # db.session.add(new_rec)
    # db.session.commit()
    records = db.session.query(DeviceData).order_by(func.max(DeviceData.id).desc()).group_by(DeviceData.dev_id)
    return render_template('index.html', records=records)


if __name__=="__main__":
    db.create_all()
    app.run(debug=True)