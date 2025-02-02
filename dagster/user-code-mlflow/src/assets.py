from dagster import asset


@asset
def users(context):
    context.log.info("Testing")
