from pathlib import Path
from dbt import context
from dagster_dbt import DbtProject

project_dir = Path(__file__).resolve()
print("project_dir: ", project_dir)
packaged_project_dir = Path(__file__).joinpath("..", "dbt-project").resolve()
print("packaged_project_dir: ", packaged_project_dir)

films_preparation_project = DbtProject(
    project_dir=project_dir,
    packaged_project_dir=packaged_project_dir,
)
films_preparation_project.prepare_if_dev()
