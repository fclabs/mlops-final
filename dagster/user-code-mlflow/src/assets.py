from dagster import (
    asset,
    multi_asset,
    AssetIn,
    Output,
    AssetDep,
    OpExecutionContext,
    AssetOut,
)
import pandas as pd

ASSETS_GROUP_NAME = "mlflow"


@asset(
    deps=[AssetDep("unified_films")],
    group_name=ASSETS_GROUP_NAME,
    required_resource_keys={"postgres_resource"},
)
def training_data(context: OpExecutionContext) -> Output[pd.DataFrame]:

    ## Source table
    ## TODO: Read from the asset metadata
    UNIFIED_FILMS_TABLE = "after_dbt.unified_films"

    query = f"SELECT * FROM {UNIFIED_FILMS_TABLE}"  # replace 'my_table' with your PostgreSQL table name
    engine = context.resources.postgres_resource

    # Use pandas to load the data from PostgreSQL into a DataFrame.
    df = pd.read_sql(query, engine)
    context.log.info(f"Loaded {len(df)} rows from PostgreSQL.")

    return Output(value=df, metadata={"num_rows": len(df)})


from dagster_mlflow import mlflow_tracking
from sklearn.model_selection import train_test_split


@multi_asset(
    ins={
        "training_data": AssetIn(
            # key_prefix=["snowflake", "core"],
            # metadata={"columns": ["id"]}
        )
    },
    outs={
        "preprocessed_training_data": AssetOut(),
        "user2Idx": AssetOut(),
        "movie2Idx": AssetOut(),
    },
    group_name=ASSETS_GROUP_NAME,
)
def preprocessed_data(training_data: pd.DataFrame):
    u_unique = training_data.user_id.unique()
    user2Idx = {o: i + 1 for i, o in enumerate(u_unique)}
    m_unique = training_data.movie_id.unique()
    movie2Idx = {o: i + 1 for i, o in enumerate(m_unique)}
    training_data["encoded_user_id"] = training_data.user_id.apply(
        lambda x: user2Idx[x]
    )
    training_data["encoded_movie_id"] = training_data.movie_id.apply(
        lambda x: movie2Idx[x]
    )

    preprocessed_training_data = training_data.copy()

    return preprocessed_training_data, user2Idx, movie2Idx
