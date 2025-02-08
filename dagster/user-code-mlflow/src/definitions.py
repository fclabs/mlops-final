import dagster as dg
import assets
from resources import postgres_resource, mlflow_resource

# Load all assets from your Airbyte instance

all_assets = dg.load_assets_from_modules([assets])

defs = dg.Definitions(
    assets=all_assets,
    resources={
        "postgres_resource": postgres_resource,
        "mlflow_resource": mlflow_resource,
    },
)
