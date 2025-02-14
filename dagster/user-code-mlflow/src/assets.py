from typing import Dict
from dagster import (
    Any,
    asset,
    multi_asset,
    AssetIn,
    Output,
    AssetDep,
    OpExecutionContext,
    AssetOut,
)
import pandas as pd
from model_helper import get_model
from tf_keras.optimizers import Adam
from matplotlib import pyplot as plt
from sklearn.metrics import mean_squared_error


ASSETS_GROUP_NAME = "mlflow"


@asset(
    deps=[AssetDep("unified_films")],
    group_name=ASSETS_GROUP_NAME,
    required_resource_keys={"postgres_resource", "postgres_query"},
)
def training_data(context: OpExecutionContext) -> Output[pd.DataFrame]:

    query = context.resources.postgres_query
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


@multi_asset(
    ins={"preprocessed_training_data": AssetIn()},
    outs={
        "X_train": AssetOut(),
        "X_test": AssetOut(),
        "y_train": AssetOut(),
        "y_test": AssetOut(),
    },
    group_name=ASSETS_GROUP_NAME,
)
def splited_data(context, preprocessed_training_data):
    test_size = 0.10
    random_state = 42
    X_train, X_test, y_train, y_test = train_test_split(
        preprocessed_training_data[["encoded_user_id", "encoded_movie_id"]],
        preprocessed_training_data[["rating"]],
        test_size=test_size,
        random_state=random_state,
    )
    return X_train, X_test, y_train, y_test


@asset(
    resource_defs={"mlflow": mlflow_tracking},
    ins={
        "X_train": AssetIn(),
        "y_train": AssetIn(),
        "user2Idx": AssetIn(),
        "movie2Idx": AssetIn(),
    },
    # config_schema={
    #     "batch_size": Int,
    #     "epochs": Int,
    #     "learning_rate": Float,
    #     "embeddings_dim": Int,
    # },
    group_name=ASSETS_GROUP_NAME,
)
def trained_model(context, X_train, y_train, user2Idx, movie2Idx):

    mlflow = context.resources.mlflow

    # batch_size = context.op_config["batch_size"]
    # epochs = context.op_config["epochs"]
    # learning_rate = context.op_config["learning_rate"]
    # embeddings_dim = context.op_config["embeddings_dim"]
    batch_size = 128
    epochs = 10
    learning_rate = 1e-3
    embeddings_dim = 5

    model = get_model(len(movie2Idx), len(user2Idx), embeddings_dim)

    model.compile(Adam(learning_rate=learning_rate), "mean_squared_error")

    context.log.info(f"batch_size: {batch_size} - epochs: {epochs}")
    history = model.fit(
        [X_train.encoded_user_id, X_train.encoded_movie_id],
        y_train.rating,
        batch_size=batch_size,
        # validation_data=([ratings_val.userId, ratings_val.movieId], ratings_val.rating),
        epochs=epochs,
        verbose=1,
    )
    for i, l in enumerate(history.history["loss"]):
        mlflow.log_metric("mse", l, i)

    fig, axs = plt.subplots(1)
    axs.plot(history.history["loss"], label="mse")
    plt.legend()
    mlflow.log_figure(fig, "plots/loss.png")
    return model


@asset(
    resource_defs={"mlflow": mlflow_tracking},
    ins={
        "trained_model": AssetIn(),
    },
    name="model_stored",
    group_name=ASSETS_GROUP_NAME,
)
def log_model(context, trained_model) -> Dict[str, Any]:
    mlflow = context.resources.mlflow

    logged_model = mlflow.tensorflow.log_model(
        trained_model,
        "keras_dot_product_model",
        registered_model_name="keras_dot_product_model",
        # input_example=[np.array([1, 2]), np.array([2, 3])],
    )
    # logged_model.flavors
    model_data = {"model_uri": logged_model.model_uri, "run_id": logged_model.run_id}
    return model_data


@asset(
    resource_defs={"mlflow": mlflow_tracking},
    ins={
        "model_stored": AssetIn(),
        "X_test": AssetIn(),
        "y_test": AssetIn(),
    },
)
def model_metrics(context, model_stored, X_test, y_test):
    mlflow = context.resources.mlflow
    logged_model = model_stored["model_uri"]

    loaded_model = mlflow.pyfunc.load_model(logged_model)

    y_pred = loaded_model.predict([X_test.encoded_user_id, X_test.encoded_movie_id])

    mse = mean_squared_error(y_pred.reshape(-1), y_test.rating.values)
    metrics = {"test_mse": mse, "test_rmse": mse ** (0.5)}
    mlflow.log_metrics(metrics)
    return metrics
