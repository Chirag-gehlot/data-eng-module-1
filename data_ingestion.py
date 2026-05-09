#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sqlalchemy import create_engine
# Using this library we'll be able to see the status of the data ingestion
from tqdm.auto import tqdm

dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}
parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

def run():
    year = 2021
    month = 1
    pg_user = 'root'
    pg_pass = 'root'
    pg_host = 'localhost'
    pg_db = 'ny_taxi'
    pg_port = 5433
    target_table = 'yellow_taxi_data'
    chunk_size = 100000
    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
    url = f'{prefix}/yellow_tripdata_{year}-{month:02d}.csv.gz'
    # Making connection to the postgre
    engine = create_engine(f"postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}")

    # Create iterator
    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        chunksize=chunk_size
    )

    # Insert chunks
    for i, df_chunk in enumerate(tqdm(df_iter)):

        if i == 0:
            # Creating a table
            # head(n=0) makes sure we only create the table, we don't add any data yet.
            df_chunk.head(n=0).to_sql(name = target_table, con=engine, if_exists='replace')

            df_chunk.to_sql(
                name=target_table,
                con=engine,
                if_exists="replace",
                index=False
            )
        else:
            df_chunk.to_sql(
                name=target_table,
                con=engine,
                if_exists="append",
                index=False
            )

        # end = time.time()

        # print(f"Finished chunk {i}")
        # print(f"Inserted rows: {len(df_chunk)}")
        # print(f"Time: {end - start:.2f} sec")


if __name__ == "__main__":
    run()

