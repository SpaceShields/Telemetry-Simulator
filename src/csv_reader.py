import csv

def read_csv():
    with open('data/tli_telemetry_mvp.csv', 'r') as file:
        reader = csv.DictReader(file)
        return list(reader)