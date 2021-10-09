from pymodbus.client.sync import ModbusSerialClient as ModbusClient

UNIT = 0x1


def run_sync_client():
    client = ModbusClient(method='rtu', port='/dev/pts/3', timeout=1,
                          baudrate=9600)
    client.connect()
    rr = client.read_holding_registers(1, 1, unit=UNIT)
    client.close()


if __name__ == "__main__":
    run_sync_client()