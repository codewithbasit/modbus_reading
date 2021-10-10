from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from app import database as db_helper
from datetime import datetime
import json
import time


def read_settings():
    settings={}
    f = open('settings.json',)
    data = json.load(f)

    if data:
        settings = data
    else:
        print("Couldn't read settings.")
    f.close()

    return settings

def read_registers(client, device_id, register_offset, num_of_regs):
    rr = client.read_holding_registers(register_offset, num_of_regs, unit=device_id)

    if rr.registers:
        return rr.registers
    else:
        return None
def run_sync_client(settings):
    data = [ ]
    device_data = {}
    client = ModbusClient(method=settings['mode'], port=settings['port'], timeout=1,
                          baudrate=settings['baudrate'])
    client.connect()
    for device in settings['devices']:
        values = read_registers(client,device['slave_id'], 
                                        device['register_offset'], 
                                        device['number_of_regs'])
        device_data['Id'] = device['slave_id']
        device_data['Description'] = device['slave_desc']
        device_data['Temperature'] = (values[0]/10.0)
        device_data['Humidity'] = (values[1]/10.0)
        data.append(device_data)
        device_data = {}

    print(data)
    client.close()
    reading_time = datetime.now()
    for item in data:
        record = db_helper.new_dev_data(item, reading_time)
        db_helper.save_record(record)

if __name__ == "__main__":
    settings = read_settings()
    if settings:
    
        while True:
            run_sync_client(settings)
            time.sleep(settings['frequency'])
    else:
        print("Configurations error.")