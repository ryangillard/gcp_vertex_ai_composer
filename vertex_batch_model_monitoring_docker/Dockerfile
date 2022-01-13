# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.8-slim

# Install python client.
# Run this the below gsutil comamnd first.
# gsutil cp gs://model_monitoring_python_client_library/aiplatform-v1beta1-py-bp.tar.gz ./content/python_client_library/aiplatform-v1beta1-py-bp.tar.gz
ADD /content /content
RUN pip3 install ./content/python_client_library/aiplatform-v1beta1-py-bp.tar.gz

# Copy local code to the container image.
COPY ./vertex_batch_model_monitoring.py ./

# Set entrypoint.
ENTRYPOINT ["python3", "./vertex_batch_model_monitoring.py"]