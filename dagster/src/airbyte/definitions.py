from dagster_airbyte import AirbyteResource, load_assets_from_airbyte_instance
import os
import dagster as dg

# Load all assets from your Airbyte instance
airbyte_assets = load_assets_from_airbyte_instance(
    # Connect to your OSS Airbyte instance
    AirbyteResource(
        host=os.environ.get("AIRBYTE_HOST", "localhost"),
        port=os.environ.get("AIRBYTE_PORT", "8000"),
    )
)

defs = dg.Definitions(
    assets=[airbyte_assets],
)
