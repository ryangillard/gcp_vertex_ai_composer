vertex_deploy_op = (
    kubernetes_pod_operator.KubernetesPodOperator(
        image="gcr.io/my-project/vertex_deploy_image:latest",
        name="vertex_deploy_pod",
        arguments=[
            '--project=my-project',
            '--region=us-central1',
            '--endpoint_display_name=docker_endpoint',
            '--model_display_name=docker_model',
            '--serving_container_image_uri=us-docker.pkg.dev/vertex-ai/prediction/tf2-cpu.2-5:latest',
            '--artifact_uri=gs://my-bucket/trained_models/autoencoder_trained',
            '--deployed_model_display_name=docker_deployed_model',
            '--machine_type=n1-standard-4',
        ],
        namespace="default",
        task_id="vertex_deploy_task",
        dag=test_dag
    )
)