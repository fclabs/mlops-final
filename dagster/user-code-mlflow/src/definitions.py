import dagster as dg
import assets
from resources import postgres_resource, postgres_query
from configs import mlflow_resources, job_training_config


all_assets = dg.load_assets_from_modules([assets])

defs = dg.Definitions(
    assets=all_assets,
    resources={
        "postgres_resource": postgres_resource,
        "postgres_query": postgres_query,
    },
    jobs=[
        dg.define_asset_job(
            "trained_model_op",
            selection=["trained_model"],
            config=job_training_config,
        ),
    ],
)
