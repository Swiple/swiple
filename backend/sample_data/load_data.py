from sqlalchemy import create_engine, schema, text
import pandas
import os

host = 'postgresql'
username = 'postgres'
password = 'postgres'
database = 'postgres'
port = 5432

engine = create_engine(
    f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
)

path_to_data = '/sample_data/data/'
schema_name = 'sample_data'

# create sample_data schema if doesn't exist
if not engine.dialect.has_schema(engine, schema_name):
    engine.execute(schema.CreateSchema(schema_name))

    # create sample data tables
    with open("/sample_data/create_tables.sql") as file:
        query = text(file.read())
        engine.execute(query)

    # read csv files and insert data into respective table
    for filename in os.listdir(path_to_data):
        if filename.endswith('.csv'):
            print(filename)
            table_name = filename.split('.')[0]

            df = pandas.read_csv(f"{path_to_data}/{filename}")
            df.to_sql(
                schema=schema_name,
                name=table_name,
                con=engine,
                if_exists='replace',
                index=False,
            )
    print("Sample data inserted.")
else:
    print("Sample data already inserted. Nothing to do.")
