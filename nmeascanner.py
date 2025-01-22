from serial import Serial
from pynmeagps import NMEAReader

with Serial('/dev/ttyS5', 9600, timeout=3) as stream:
    nmr = NMEAReader(stream)
    while True:
        raw_data, parsed_data = nmr.read()
        if parsed_data is not None:
            print(parsed_data)
        else:
            break