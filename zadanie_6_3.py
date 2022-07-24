""" Skorzystaj z danych clean_stations.csv oraz clean_measure.csv. 
Na podstawie tych zbiorów stwórz bazę danych i tabelę, 
do której będzie można się odwoływać, na przykład poprzez wywołanie:
conn.execute("SELECT * FROM stations LIMIT 5").fetchall()"""
# Wykorzystam kod ze strony https://stackoverflow.com/questions/31394998/using-sqlalchemy-to-load-csv-file-into-a-database

import csv
import pandas as pd
from sqlalchemy import create_engine

# Create engine to connect with DB
try:
    engine = create_engine('sqlite:///stations.db')
except:
    print("Can't create 'engine")

# Get data from CSV file to DataFrame(Pandas)
with open('clean_stations.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    columns = [
         'station',
         'latitude',
         'longitude',
         'elevation',
         'name',
         'country',
         'state'
    ]
    df = pd.DataFrame(data=reader, columns=columns)

# Standart method of Pandas to deliver data from DataFrame to PastgresQL
try:
    with engine.begin() as connection:
        # Jaka jest konwencja nazywania tabel?
        df.to_sql('stations', con=connection, index_label='id', if_exists='replace')
        print('Done, ok!')
except:
    print('Something went wrong!')

with open('clean_measure.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    columns = [
         'station',
         'date',
         'precip',
         'tobs'
    ]
    df = pd.DataFrame(data=reader, columns=columns)

# Standart method of Pandas to deliver data from DataFrame 
try:
    with engine.begin() as connection:
        df.to_sql('measures', con=connection, index_label='id', if_exists='replace')
        print('Done, ok!')
except:
    print('Something went wrong!')

conn = engine.connect()
result = conn.execute("SELECT * FROM stations LIMIT 10").fetchall()

for row in result:
   print(row)

# Czy używa się dwa razy tej samej zmiennej czy powinnam napisać np. result_1?
result = conn.execute("SELECT * FROM measures WHERE station = 'USC00517948' ").fetchall()

for row in result:
   print(row)