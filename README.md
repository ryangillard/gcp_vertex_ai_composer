# gcp_vertex_ai_composer
Vertex AI via Cloud Composer

## vertex_batch_model_monitoring
This component type creates batch model monitoring jobs using an uploaded model in Vertex AI, input data either in GCS or BigQuery, as well as training data for training-serving skew alerts and a schema.

`project`: str, GCP project to perform batch predictions for.

`region`: str, GCP project to perform batch predictions for.

`model_id`: str, Vertex AI model ID.

`job_display_name`: str, display name for batch prediction job.

`instances_format`: str, format of prediction input instances. Choices are "jsonl", "csv", "bigquery", "tf-record", "tf-record-gzip", and "file-list".

`gcs_source`: str, GCS URI to input data for batch prediction.

`predictions_format`: str, format of predictions. Choices are "jsonl", "csv", and "bigquery".

`gcs_destination_prefix`: str, GCS URI prefix to use as destination location.

`training_dataset_format`: str, format of training dataset to use for skew detection. Choices are "csv" and "bigquery".

`training_dataset_uri`: str, URI to training dataset to use for skew detection.

`analysis_instance_schema_yaml_uri`: str, YAML schema indicating feature types when doing analysis.

`machine_type`: str, the machine type to use for the batch prediction workers.

`starting_replica_count`: int, number of worker replicas to start with.

`max_replica_count`: int, ax number of worker replicas to scale to.

`accelerator_type`: str, accelerator type to use for job. Current accelerator types.

`accelerator_count`: int, number of accelerators to use per worker replica.

`feature_list`: str, comma-separated list of feature names.

`default_threshold_value`: float, default threshold value for alerts.

`custom_threshold_dict`: str, JSON formatted dictionary: key=feature name, value=thresholds.

`email_address`: str, Email address to send alerts to.

`job_polling_frequency`: int, number of seconds to wait between job status polls.


## vertex_batch_predict
This component type creates batch prediction jobs using an uploaded model in Vertex AI and input data either in GCS or BigQuery.

Note: For batch predictions using custom containers, the format of each instance currently is limited to an array/list of values. Keyed features already work for online predictions and will be eventually added for batch predictions.

`project`: str, GCP project to perform batch predictions for.

`region`: str, GCP project to perform batch predictions for.

`model_display_name`: str, display name of uploaded model.

`job_display_name`: str, display name for batch prediction job.

`instances_format`: str, format of prediction input instances. Choices are "jsonl", "csv", "bigquery", "tf-record", "tf-record-gzip", and "file-list".

`predictions_format`: str, format of predictions. Choices are "jsonl", "csv", and "bigquery".

`gcs_source`: str, GCS URI to input data for batch prediction.

`gcs_destination_prefix`: str, GCS URI prefix to use as destination location.

`machine_type`: str, the machine type to use for the batch prediction workers.


## vertex_deploy
This component type deploys Vertex AI uploaded model for online predictions.

`project`: str, GCP project to deploy uploaded Vertex model.

`region`: str, GCP region to deploy uploaded Vertex model.

`endpoint_display_name`: str, name to display of the endpoint to use for the deployed model.

`model_display_name`: str, name of Vertex AI uploaded model to deploy to endpoint.

`deployed_model_display_name`: str, name to display for deployed model.

`machine_type`: str, the machine type to use for the online prediction workers.


## vertex_export_model
This component type exports models from Vertex AI to either artifacts in GCS or images in GCR.

`project`: str, GCP project to deploy uploaded Vertex model.

`region`: str, GCP region to deploy uploaded Vertex model.

`model_id`: str, model ID to export.

`model_display_name`: str, name of model to export. Can be used if the model_id is not known.

`export_format_id`: str, name to display for deployed model. Choices are "tflite", "edgetpu-tflite", "tf-saved-model", "tf-js", "core-ml", and "custom-trained".

`destination_type`: str, whether model should be exported as an artifact to GCS or an image to GCR.

`destination_path`: str, GCS or GCR path where to export model artifact or image.


## vertex_hptuning
This component type performs hyperparameter tuning to find the hyperparameters that give the best model performance using Vertex AI.

`ml_framework`: str, ML framework to use for training. Choices are "tensorflow", "pytorch", "xgboost", "sklearn", "lightgbm", "tpot".

`project`: str, GCP project to use for quota/billing for vertex training.

`region`: str, GCP region to run vertex training. Ensure your project has available quota in that region.

`job_display_name`: str, display name for Vertex training job.

`replica_count`: int, number of worker replicas to use for Vertex training job.

`pre_built_training_container_uri`: str, pre-built training container URI. For example, this could be a base tensorflow image but not a custom image. Can't use if also using custom_training_container_uri.

`model_package_gcs_path`: str, GCS path to model package location. Model package should be a source distribution of a python package of a model of type tar.gz.

`python_module`: str, python module package path. For example, "trainer.task".

`custom_training_container_uri`: str, custom training container URI. For example, would be a custom image that contains all necessary packages and dependencies. Can't use if also using pre_built_training_container_uri.

`machine_type`: str, the machine type to use for the Vertex training job workers.

`accelerator_type`: str, accelerator type to use for Vertex training job. Current accelerator types.

`accelerator_count`: int, number of accelerators to use per worker replica.

`job_polling_frequency`: int, number of seconds to wait between job status polls.

`trainer_args`: dict, dictionary of arguments to be used by trainer module.

`metric_id`: str, name of metric to optimize, i.e. accuracy.

`goal_type`: str, the optimization goal. Choices are "minimize" and "maximize".

`algorithm`: str, search algorithm to use between trials. Choices are "bayesian", "random", and "grid".

`parameters`: list, hyperparameter configs to tune. Read in as a JSON string.

`max_trial_count`: int, total number of trials to run.

`parallel_trial_count`: int, number of parallel trials that can run simultaneously.


## vertex_train
This component type trains model packages of various frameworks using Vertex AI.

`ml_framework`: str, ML framework to use for training. Choices are "tensorflow", "pytorch", "xgboost", "sklearn", "lightgbm", "tpot".

`project`: str, GCP project to use for quota/billing for vertex training.

`region`: str, GCP region to run vertex training. Ensure your project has available quota in that region.

`job_display_name`: str, display name for Vertex training job.

`replica_count`: int, number of worker replicas to use for Vertex training job.

`pre_built_training_container_uri`: str, pre-built training container URI. For example, this could be a base tensorflow image but not a custom image. Can't use if also using custom_training_container_uri.

`model_package_gcs_path`: str, GCS path to model package location. Model package should be a source distribution of a python package of a model of type tar.gz.
`python_module`: str, python module package path. For example, "trainer.task".

`custom_training_container_uri`: str, custom training container URI. For example, would be a custom image that contains all necessary packages and dependencies. Can't use if also using pre_built_training_container_uri.

`machine_type`: str, the machine type to use for the Vertex training job workers.

`accelerator_type`: str, accelerator type to use for Vertex training job. Current accelerator types.

`accelerator_count`: int, number of accelerators to use per worker replica.

`job_polling_frequency`: int, number of seconds to wait between job status polls.

`trainer_args`: dict, dictionary of arguments to be used by trainer module.


## vertex_upload_model
This component type uploads trained model artifacts to Vertex AI.

`ml_framework`: str, ML framework to use for prediction. Choices are "tensorflow", "pytorch", "xgboost", "sklearn", "lightgbm", "tpot".

`project`: str, GCP project to deploy uploaded Vertex model.

`region`: str, GCP region to deploy uploaded Vertex model.

`model_display_name`: str, name to display for uploaded model. Cannot cannot certain special characters such as ".".

`serving_container_image_uri`: str, serving container image URI to use for predictions. For example, this could be a base tensorflow image or a custom image that contains all necessary packages and dependencies.

`artifact_uri`: str, GCS URI of trained model artifacts. Note this is just the directory that contains the artifacts.

`custom_serving_container_health_route`: str, HTTP path on the container to send health checks to. Only needs to be set for custom container predictions.

`custom_serving_container_predict_route`: str, HTTP path on the container to send prediction requests to. Only needs to be set for custom container predictions.
