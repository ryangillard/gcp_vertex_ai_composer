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
        help="Name of model to export.",
        type=str,
        default=""
    )
    parser.add_argument(
        "--model_id",
        help="Model ID to export.",
        type=str,
        default=""
    )
    parser.add_argument(
        "--export_format_id",
        help="Type of export format.",
        type=str,
        choices=[
            "tflite",
            "edgetpu-tflite",
            "tf-saved-model",
            "tf-js",
            "core-ml",
            "custom-trained"
        ],
        default="custom-trained"
    )
    parser.add_argument(
        "--destination_type",
        help="Whether model should be exported as an artifact to GCS or an image to GCR.",
        type=str,
        choices=["gcs", "gcr"],
        default="gcs"
    )
    parser.add_argument(
        "--destination_path",
        help="GCS or GCR path where to export model artifact or image.",
        type=str,
        required=True
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


def export_model(arguments):
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

    # Finally export model.
    if arguments["destination_type"] == "gcs":
        response = model.export_model(
            export_format_id=arguments["export_format_id"],
            artifact_destination=arguments["destination_path"]
        )
    else:
        response = model.export_model(
            export_format_id=arguments["export_format_id"],
            image_destination=arguments["destination_path"]
        )
    print("Model export response = {}".format(response))


if __name__ == "__main__":
    arguments = parse_command_line_arguments()
    export_model(arguments)
