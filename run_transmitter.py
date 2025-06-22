import sys
import os

apid = 100
seq_count = 42
payload_length = 32

# Add the src path to use nested files
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import the required functions from the src folder
from csv_reader import read_csv
from packet_encoder import encode_primary_header, encode_secondary_header

csv_data = read_csv()

# Sanity Test
for row in csv_data:
    print(row)
    break

header = encode_primary_header(apid, seq_count, payload_length)
sec_header = encode_secondary_header(csv_data[3])
print(header.hex())
print(sec_header.hex())

# transmitter = Transmitter(csv_data)
# transmitter.transmit()