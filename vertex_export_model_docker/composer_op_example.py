vertex_export_model_op = (
    kubernetes_pod_operator.KubernetesPodOperator(
        image="gcr.io/my-project/vertex_export_model_image:latest",
        name="vertex_export_model_pod",
        arguments=[
            '--project=my-project',
            '--region=us-central1',
            '--model_display_name=docker_model',
            '--export_format_id=custom-trained',
            '--destination_type=gcs',
            '--destination_path=gs://my-bucket/exported_models',
        ],
        namespace="default",
        task_id="vertex_export_model_task",
        dag=test_dag
    )
)
    