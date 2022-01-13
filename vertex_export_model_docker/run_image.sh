#!/bin/bash

docker run -it --rm \
    gcr.io/my-project/vertex_export_model_image:latest \
    --project=my-project \
    --region=us-central1 \
    --model_display_name=docker_model \
    --export_format_id=custom-trained \
    --destination_type=gcs \
    --destination_path=gs://my-bucket/exported_models