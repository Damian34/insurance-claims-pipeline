FROM apache/airflow:3.2.1-python3.14

USER root
RUN mkdir -p /opt/airflow/data && chown -R airflow:root /opt/airflow/data

USER airflow
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && rm requirements.txt