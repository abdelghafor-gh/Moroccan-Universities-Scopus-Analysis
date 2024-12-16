FROM apache/airflow:2.7.3-python3.10

# Install required packages for building Python packages
USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Switch back to airflow user
USER airflow

# Install only the required Python packages for the ETL pipeline
COPY requirements-airflow.txt /opt/airflow/requirements-airflow.txt
RUN pip install --no-cache-dir -r /opt/airflow/requirements-airflow.txt
