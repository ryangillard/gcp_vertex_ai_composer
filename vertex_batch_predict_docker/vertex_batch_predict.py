import argparse

from google.cloud import aiplatform


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
        "--model_display_name",
        help="Name of model to upload trained model to.",
        type=str,
        default=""
    )
    parser.add_argument(
        "--model_id",
        help="Previously created model ID to use.",
        type=str,
        default=""
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
        "--predictions_format",
        help="Format of predictions.",
        type=str,
        choices=["jsonl", "csv", "bigquery"],
        default="jsonl"
    )
    parser.add_argument(
        "--gcs_source",
        help="GCS path of source input data.",
        type=str,
        required=True
    )
    parser.add_argument(
        "--gcs_destination_prefix",
        help="GCS path prefix to store predictions.",
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


def batch_predict_from_deployed_model(arguments):
    # Initialize.
    aiplatform.init(
        project=arguments["project"], location=arguments["region"]
    )

    # Get model ID.
    model_id = arguments["model_id"]
    if not model_id:
        model_display_name = arguments["model_display_name"]
        model_name_match = aiplatform.Model.list(
            filter="display_name={}".format(model_display_name)
        )
        if not model_name_match:
            print(
                "Model with name {} does NOT exist!".format(
                    model_display_name
                )
            )
            return
        else:
            model_id = model_name_match[0].name.split("/")[-1]
    print("Model ID = {}".format(model_id))

    # Fetch Model object.
    model = aiplatform.Model(model_name=model_id)

    # Call batch_predict method of Model.
    batch_prediction_job = model.batch_predict(
        instances_format=arguments["instances_format"],
        predictions_format=arguments["predictions_format"],
        job_display_name=arguments["job_display_name"],
        gcs_source=arguments["gcs_source"],
        gcs_destination_prefix=arguments["gcs_destination_prefix"],
        model_parameters=None,
        machine_type=arguments["machine_type"],
        starting_replica_count=arguments["starting_replica_count"],
        max_replica_count=arguments["max_replica_count"],
        sync=True
    )
    print("Batch prediction job = {}".format(batch_prediction_job))


if __name__ == "__main__":
    arguments = parse_command_line_arguments()
    batch_predict_from_deployed_model(arguments)
