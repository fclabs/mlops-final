import dagster as dg
import assets

# Load all assets from your Airbyte instance

all_assets = dg.load_assets_from_modules([assets])

defs = dg.Definitions(
    assets=all_assets,
)
