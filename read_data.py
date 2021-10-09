from pymodbus.client.sync import ModbusSerialClient as ModbusClient

units = [41,42,43,44]


def run_sync_client():
    client = ModbusClient(method='rtu', port='COM3', timeout=1,
                          baudrate=9600)
    client.connect()
    for unit in units:
        rr = client.read_holding_registers(12, 2, unit=unit)
        print(unit)
        print(rr.registers)
    client.close()


if __name__ == "__main__":
    run_sync_client()