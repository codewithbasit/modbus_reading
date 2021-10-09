from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import json

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

def run_sync_client(settings):
    data = []
    device_data = {}
    
    client = ModbusClient(method=settings['mode'], port=settings['port'], timeout=1,
                          baudrate=settings['baudrate'])
    client.connect()
    for device in settings['devices']:
        rr = client.read_holding_registers(device['register_offset'], 
                                            device['number_of_regs'], 
                                            unit=device['slave_id'])
        device_data['Id'] = device['slave_id']
        device_data['Temperature'] = (rr.registers[0]/100)
        device_data['Humidity'] = (rr.registers[1]/100)
        data.append(device_data)

    print(data)
    client.close()


if __name__ == "__main__":
    settings = read_settings()
    if settings:
        run_sync_client(settings)
    else:
        print("Configurations error.")