vertex_batch_predict_op = (
    kubernetes_pod_operator.KubernetesPodOperator(
        image="gcr.io/my-project/vertex_batch_predict_image:latest",
        name="vertex_batch_predict_pod",
        arguments=[
            '--project=my-project',
            '--region=us-central1',
            '--model_display_name=test_model',
            '--job_display_name=vertex-batch-predict',
            '--instances_format=csv',
            '--predictions_format=jsonl',
            '--gcs_source=gs://my-bucket/data/test_data.csv',
            '--gcs_destination_prefix=gs://my-bucket/model_monitoring',
            '--machine_type=n1-standard-4',
        ],
        namespace="default",
        task_id="vertex_batch_predict_task",
        dag=test_dag
    )
)