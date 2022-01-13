#!/bin/bash

docker run -it --rm \
    gcr.io/my-project/vertex_upload_model_image:latest \
    --project=my-project \
    --region=us-central1 \
    --model_display_name=uploaded_model \
    --serving_container_image_uri=us-docker.pkg.dev/vertex-ai/prediction/tf2-cpu.2-5:latest \
    --artifact_uri=gs://my-bucket/trained_models/autoencoder_trained