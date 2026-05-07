import pendulum
from airflow.sdk import dag, task

from src.claim_analyzer import ClaimAnalyzer
from src.claim_normalizer import ClaimNormalizer
from src.source_loader import SourceLoader


@dag(
    dag_id="insurance_claim_pipeline",
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    schedule="*/1 * * * *", # schedule="*/5 * * * *",
    catchup=True,
    max_active_runs=1,
    tags=["dev", "insurance_claim_dag"],
)
def insurance_claim_dag():
    @task()
    def extract():
        print("extract task!")
        loader = SourceLoader()
        loader.download_file()

    @task()
    def transform():
        print("transform task!")
        loader = SourceLoader()
        normalizer = ClaimNormalizer()
        # reads file and saves normalized data to silver layer
        for raw in loader.get_insurance_claims_data():
            normalized = normalizer.normalize(raw)
            # save to silver layer...

    @task()
    def load():
        print("load task!")
        analyzer = ClaimAnalyzer()
        # reads from silver layer, enriches and saves to gold layer

    extract() >> transform() >> load()

# DAG must be called for Airflow to discover it
insurance_claim_dag()
