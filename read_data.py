from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import json

settings={}

def read_settings():
    f = open('settings.json',)
    data = json.load(f)

    if data:
        settings = data
    else:
        print("Couldn't read settings.")
    f.close()

def run_sync_client():
    client = ModbusClient(method=settings['mode'], port=settings['port'], timeout=1,
                          baudrate=settings['baudrate'])
    client.connect()
    for device in settings['devices']:
        rr = client.read_holding_registers(device['register_offset'], 
                                            device['number_of_regs'], 
                                            unit=device['slave_id'])
        print(unit=device['slave_id'])
        print(rr.registers)
    client.close()


if __name__ == "__main__":
    read_settings()
    if settings:
        run_sync_client()
    else:
        print("Configurations error.")