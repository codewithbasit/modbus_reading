from app import db
from sqlalchemy.sql import func
from datetime import datetime

class DeviceData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dev_id = db.Column(db.Integer)
    dev_desc = db.Column(db.String(255))
    dev_temp = db.Column(db.Float)
    dev_hum = db.Column(db.Float)
    reading_time = db.Column(db.DateTime(timezone=True), nullable=False)
    
def new_dev_data(data, time):
    new_data = DeviceData(
        dev_id = data['Id'],
        dev_desc = data['Description'],
        dev_temp = data['Temperature'],
        dev_hum = data['Humidity'],
        reading_time = time
    )
    
    return new_data

def save_record(rec):
    db.session.add(rec)
    db.session.commit()
    
def get_latest_records():
    records = db.session.query(DeviceData).order_by(func.max(DeviceData.id).desc()).group_by(DeviceData.dev_id)
    return records