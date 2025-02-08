from dagster import Definitions, AssetKey
from dagster_dbt import DbtCliResource
from assets import films_preparation_dbt_assets
from project import films_preparation_project
from schedules import schedules


defs = Definitions(
    assets=[films_preparation_dbt_assets],
    schedules=schedules,
    resources={
        "dbt": DbtCliResource(project_dir=films_preparation_project),
    },
)
