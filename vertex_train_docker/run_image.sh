#!/bin/bash

docker run -it --rm \
    gcr.io/my-project/vertex_train_image:latest \
    --ml_framework=tensorflow \
    --project=my-project \
    --region=us-central1 \
    --job_display_name=test-experiment \
    --replica_count=1 \
    --pre_built_training_container_uri=us-docker.pkg.dev/vertex-ai/training/tf-gpu.2-5:latest \
    --model_package_gcs_path=gs://my-bucket/model_code/test_model-0.1.tar.gz \
    --python_module=trainer.task \
    --machine_type=n1-standard-4 \
    --accelerator_type=NVIDIA_TESLA_K80 \
    --accelerator_count=1 \
    --job_polling_frequency=15 \
    --trainer_args='{"train_file_pattern": "gs://my-bucket/data/train_data.csv*", "eval_file_pattern": "gs://my-bucket/data/eval_data.csv*", "train_dataset_length": 10000, "num_epochs": 2, "train_batch_size": 100, "eval_batch_size": 100, "num_columns": 5, "hidden_units": [32, 16, 8], "learning_rate": 0.01, "output_dir": "gs://my-bucket/trained_models/tensorflow"}'