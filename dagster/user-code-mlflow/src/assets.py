from dagster import asset, AssetKey, AssetIn


# @asset(ins={"unified_films": AssetIn(key=("default", "unified_films"))})
# def training_data(unified_films): ...
