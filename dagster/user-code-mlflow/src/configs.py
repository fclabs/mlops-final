import os


def get_mlflow_uri():
    hostname = os.environ.get("MLFLOW_HOSTNAME", "mlflow")
    port = os.environ.get("MLFLOW_PORT", "5000")
    return f"http://{hostname}:{port}"


mlflow_resources = {
    "mlflow": {
        "config": {
            "experiment_name": "recommender_system",
            "mlflow_tracking_uri": get_mlflow_uri(),
        }
    },
}

training_config = {
    "trained_model": {
        "config": {
            "batch_size": 128,
            "epochs": 10,
            "learning_rate": 1e-3,
            "embeddings_dim": 5,
        }
    }
}

job_training_config = {"resources": {**mlflow_resources}, "ops": {**training_config}}
