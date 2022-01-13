#!/bin/bash

docker run -it --rm \
    gcr.io/my-project/vertex_batch_predict_image:latest \
    --project=my-project \
    --region=us-central1 \
    --model_display_name=test_model \
    --job_display_name=vertex-batch-predict \
    --instances_format=csv \
    --predictions_format=jsonl \
    --gcs_source=gs://my-bucket/data/eval_data.csv \
    --gcs_destination_prefix=gs://my-bucket/batch_predictions_docker \
    --machine_type=n1-standard-4