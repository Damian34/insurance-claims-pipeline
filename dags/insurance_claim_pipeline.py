import pendulum
from airflow.sdk import dag, task

from src.claim_analyzer import ClaimAnalyzer
from src.claim_normalizer import ClaimNormalizer
from src.claim_repository import ClaimRepository
from src.source_loader import SourceLoader
from src.logger_cfg import logg

BATCH_SIZE = 100

@dag(
    dag_id="insurance_claim_pipeline",
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    schedule="*/5 * * * *",
    catchup=True,
    max_active_runs=1,
    tags=["dev", "insurance_claim_dag"],
)
def insurance_claim_dag():
    @task()
    def extract():
        logg.info("start extract task!")
        loader = SourceLoader()
        loader.download_file()

    @task()
    def transform():
        logg.info("start transform task!")
        loader = SourceLoader()
        normalizer = ClaimNormalizer()
        repository = ClaimRepository()
        # reads file and saves normalized data to silver layer
        batch = []
        for raw_data in loader.get_insurance_claims_data():
            normalized = normalizer.normalize(raw_data)
            if normalized:
                batch.append(normalized)
                if len(batch) == BATCH_SIZE:
                    repository.save_claims_silver(batch)
                    batch = []
        repository.save_claims_silver(batch)

    @task()
    def load():
        logg.info("load transform task!")
        analyzer = ClaimAnalyzer()
        repository = ClaimRepository()
        # reads from silver layer, enriches and saves to gold layer
        batch = []
        for record in repository.load_claims_silver():
            enriched = analyzer.calculate_and_enrich(record)
            batch.append(enriched)
            if len(batch) == BATCH_SIZE:
                repository.save_claims_gold(batch)
                batch = []
        repository.save_claims_gold(batch)

    extract() >> transform() >> load()

# DAG must be called for Airflow to discover it
insurance_claim_dag()
