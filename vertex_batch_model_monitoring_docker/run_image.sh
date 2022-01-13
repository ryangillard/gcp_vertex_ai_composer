#!/bin/bash

docker run -it --rm \
    gcr.io/mlops-scrath-abed31/vertex_batch_model_monitoring_image:latest \
    --project=my-project \
    --region=us-central1 \
    --job_display_name=vertex-batch-model-monitoring \
    --instances_format=csv \
    --gcs_source=gs://my-bucket/data/test_data.csv \
    --predictions_format=jsonl \
    --gcs_destination_prefix=gs://my-bucket/model_monitoring \
    --training_dataset_format=csv \
    --training_dataset_uri=gs://my-bucket/data/train_data.csv \
    --analysis_instance_schema_yaml_uri=gs://my-bucket/data/schema.yaml \
    --machine_type=n1-standard-4 \
    --starting_replica_count=1 \
    --max_replica_count=1 \
    --feature_list=feat_0 \feat_1 \feat_2 \feat_3 \feat_4 \
    --default_threshold_value=0.001 \
    --custom_threshold_dict={"feat_2": 0.8} \
    --email_address=ryangillard@google.com \
    --job_polling_frequency=15 \