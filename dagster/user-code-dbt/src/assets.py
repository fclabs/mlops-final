from dagster import AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets
from project import films_preparation_project


@dbt_assets(manifest=films_preparation_project.manifest_path)
def films_preparation_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
