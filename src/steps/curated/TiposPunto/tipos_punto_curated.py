def run(base_parameters):

    source_bucket = base_parameters.get("source_bucket")
    target_bucket = base_parameters.get("target_bucket")

    print(f"Bucket de origen: {source_bucket}")
    print(f"Bucket de destino: {target_bucket}")
