import argparse
import json
import time

from google.cloud.aiplatform_v1beta1.services import job_service
from google.cloud.aiplatform_v1beta1.types import accelerator_type
from google.cloud.aiplatform_v1beta1.types import batch_prediction_job
from google.cloud.aiplatform_v1beta1.types import io
from google.cloud.aiplatform_v1beta1.types import machine_resources
from google.cloud.aiplatform_v1beta1.types import model_monitoring


def parse_arguments(parser):
    """Parses command line arguments.

    Args:
        parser: instance of `argparse.ArgumentParser`.
    """
    parser.add_argument(
        "--project",
        help="GCP project to deploy model to.",
        type=str,
        required=True
    )
    parser.add_argument(
        "--region",
        help="Region to deploy model in.",
        type=str,
        default="us-central1"
    )
    parser.add_argument(
        "--model_id",
        help="Vertex AI model ID.",
        type=str,
        required=True
    )
    parser.add_argument(
        "--job_display_name",
        help="Display name of batch prediction job.",
        type=str,
        default=""
    )
    parser.add_argument(
        "--instances_format",
        help="Format of input data instances.",
        type=str,
        choices=["jsonl", "csv", "bigquery", "tf-record", "tf-record-gzip", "file-list"],
        default="jsonl"
    )
    parser.add_argument(
        "--gcs_source",
        help="GCS path of source input data.",
        type=str,
        required=True
    )
    parser.add_argument(
        "--predictions_format",
        help="Format of predictions.",
        type=str,
        choices=["jsonl", "csv", "bigquery"],
        default="jsonl"
    )
    parser.add_argument(
        "--gcs_destination_prefix",
        help="GCS path prefix to store predictions.",
        type=str,
        required=True
    )
    parser.add_argument(
        "--training_dataset_format",
        help="Format of training dataset to use for skew detection.",
        type=str,
        choices=["csv", "bigquery"],
        default="csv"
    )
    parser.add_argument(
        "--training_dataset_uri",
        help="URI to training dataset to use for skew detection.",
        type=str,
        required=True
    )
    parser.add_argument(
        "--analysis_instance_schema_yaml_uri",
        help="YAML schema indicating feature types when doing analysis.",
        type=str,
        required=True
    )
    parser.add_argument(
        "--machine_type",
        help="Machine type for the workers.",
        type=str,
        default="n1-standard-4"
    )
    parser.add_argument(
        "--starting_replica_count",
        help="Number of worker replicas to start with.",
        type=int,
        default=1
    )
    parser.add_argument(
        "--max_replica_count",
        help="Max number of worker replicas to scale to.",
        type=int,
        default=1
    )
    parser.add_argument(
        "--accelerator_type",
        help="Accelerator type.",
        type=str,
        default=""
    )
    parser.add_argument(
        "--accelerator_count",
        help="Number of accelerators to use.",
        type=int,
        default=0
    )
    parser.add_argument(
        "--feature_list",
        help="Comma-separated list of feature names.",
        type=str,
        default=""
    )
    parser.add_argument(
        "--default_threshold_value",
        help="Default threshold value for alerts.",
        type=float,
        default=0.001
    )
    parser.add_argument(
        "--custom_threshold_dict",
        help="JSON formatted dictionary: key=feature name, value=thresholds.",
        type=json.loads,
        default=""
    )
    parser.add_argument(
        "--email_address",
        help="Email address to send alerts to.",
        type=str,
        required=True
    )
    parser.add_argument(
        "--job_polling_frequency",
        help="Number of seconds to wait between job status polls.",
        type=int,
        default=15
    )


def parse_command_line_arguments():
    """Parses command line arguments and returns dictionary.

    Returns:
        Dictionary containing command line arguments.
    """
    parser = argparse.ArgumentParser()

    # Add arguments to parser.
    parse_arguments(parser)

    # Parse all arguments.
    args = parser.parse_args()
    arguments = args.__dict__

    return arguments


def get_thresholds(feature_list, default_threshold_value, custom_threshold_dict):
    """Gets thresholds.

    Args:
        feature_list: str, comma-separated string list of feature names.
        default_threshold_value: float, default value to use for thresholds.
        custom_threshold_dict: dict, custom thresholds stored in dict with
            keys being the feature names and values being the thresholds.

    Returns:
        Dictionary of `model_monitoring.ThresholdConfig`s keyed on features.
    """
    thresholds = {
        k: model_monitoring.ThresholdConfig(value=float(v))
        for k, v in custom_threshold_dict.items()
    }
    for feature in feature_list.split(","):
        if feature not in thresholds:
            thresholds[feature] = model_monitoring.ThresholdConfig(
                value=float(default_threshold_value)
            )
    return thresholds


def get_dedicated_resources(arguments):
    """Gets dedicated compute resources.

    Args:
        arguments: dict, user passed parameters.

    Returns:
        A `machine_resources.BatchDedicatedResources` object.

    """
    # Get accelerator_type.
    accelerator_map = {
        "NVIDIA_TESLA_K80": accelerator_type.AcceleratorType.NVIDIA_TESLA_K80,
        "NVIDIA_TESLA_P100": accelerator_type.AcceleratorType.NVIDIA_TESLA_P100,
        "NVIDIA_TESLA_V100": accelerator_type.AcceleratorType.NVIDIA_TESLA_V100,
        "NVIDIA_TESLA_P4": accelerator_type.AcceleratorType.NVIDIA_TESLA_P4,
        "NVIDIA_TESLA_T4": accelerator_type.AcceleratorType.NVIDIA_TESLA_T4
    }
    accel_type = accelerator_map.get(arguments["accelerator_type"])
    machine_spec = machine_resources.MachineSpec(machine_type=arguments["machine_type"])
    if accel_type is None:
        machine_spec = machine_resources.MachineSpec(
            machine_type=arguments["machine_type"],
            accelerator_count=arguments["accelerator_count"],
            accelerator_type=accel_type,
        )
    dedicated_resources = machine_resources.BatchDedicatedResources(
            machine_spec=machine_spec,
            starting_replica_count=arguments["starting_replica_count"],
            max_replica_count=arguments["max_replica_count"],
        )
    return dedicated_resources


def create_batch_model_monitoring_job(arguments):
    """Creates batch model monitoring job.

    Args:

        arguments: dict, user passed parameters.
    """
    # The AI Platform services require regional API endpoints.
    client_options = {
        "api_endpoint": "{}-aiplatform.googleapis.com".format(
            arguments["region"]
        )
    }

    # Initialize client that will be used to create and send requests.
    # This client only needs to be created once, and can be reused for multiple requests.
    client = job_service.JobServiceClient(client_options=client_options)

    parent = "projects/{project}/locations/{location}".format(
          project=arguments["project"], location=arguments["region"]
    )

    input_config = batch_prediction_job.BatchPredictionJob.InputConfig(
        instances_format=arguments["instances_format"],
        gcs_source=io.GcsSource(uris=[arguments["gcs_source"]])
    )

    output_config = batch_prediction_job.BatchPredictionJob.OutputConfig(
        predictions_format=arguments["predictions_format"],
        gcs_destination=io.GcsDestination(
            output_uri_prefix=arguments["gcs_destination_prefix"]
        )
    )

    training_dataset = (
        model_monitoring.ModelMonitoringObjectiveConfig.TrainingDataset(
            data_format=arguments["training_dataset_format"],
            gcs_source=io.GcsSource(uris=[arguments["training_dataset_uri"]])
        )
    )

    training_prediction_skew_detection_config = (
        model_monitoring.ModelMonitoringObjectiveConfig.TrainingPredictionSkewDetectionConfig(
            skew_thresholds=get_thresholds(
                arguments["feature_list"],
                arguments["default_threshold_value"],
                arguments["custom_threshold_dict"]
            )
        )
    )

    objective_config = model_monitoring.ModelMonitoringObjectiveConfig(
        training_dataset=training_dataset, 
        training_prediction_skew_detection_config=(
            training_prediction_skew_detection_config
        )
    )

    alert_config = model_monitoring.ModelMonitoringAlertConfig(
        email_alert_config=(
            model_monitoring.ModelMonitoringAlertConfig.EmailAlertConfig(
                user_emails=[arguments["email_address"]]
            )
        )
    )

    monitoring_config = model_monitoring.ModelMonitoringConfig(
        objective_configs=[objective_config],
        alert_config=alert_config,
        analysis_instance_schema_uri=arguments["analysis_instance_schema_yaml_uri"]
    )

    batch_predict_job = batch_prediction_job.BatchPredictionJob(
        display_name=arguments["job_display_name"],
        model="projects/{}/locations/{}/models/{}".format(
            arguments["project"], arguments["region"], arguments["model_id"]
        ),
        input_config=input_config,
        output_config=output_config,
        dedicated_resources=get_dedicated_resources(arguments),
        model_monitoring_config=monitoring_config
    )

    response = client.create_batch_prediction_job(
            parent=parent, batch_prediction_job=batch_predict_job
    )
    print("Batch model monitoring job = {}".format(response))

    # Wait for job to terminate.
    running_states = set([1, 2, 3, 8])
    completed_state = 4
    while True:
        state = client.get_batch_prediction_job(name=response.name).state
        if state not in running_states:
            break
        time.sleep(arguments["job_polling_frequency"])
    assert state == completed_state, "Job did not complete successfully."


if __name__ == "__main__":
    arguments = parse_command_line_arguments()
    create_batch_model_monitoring_job(arguments)
