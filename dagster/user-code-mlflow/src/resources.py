from dagster import resource
import sqlalchemy
import os


@resource
def postgres_resource(context):
    # The connection string is provided via resource config.
    # For example: "postgresql://user:password@hostname:5432/mydatabase"
    user = os.environ.get("POSTGRES_USER", "postgres")
    password = os.environ.get("POSTGRES_PASSWORD", "postgres")
    hostname = os.environ.get("POSTGRES_HOSTNAME", "postgres")
    database = os.environ.get("POSTGRES_DB", "mlops")
    connection_string = f"postgresql://{user}:{password}@{hostname}:5432/{database}"
    engine = sqlalchemy.create_engine(connection_string)
    return engine


@resource
def postgres_query(context):

    return "SELECT * FROM after_dbt.unified_films"  # replace 'my_table' with your PostgreSQL table name
