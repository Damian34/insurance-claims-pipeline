from pathlib import Path

import duckdb
import kagglehub
from typing import Generator, Any
from src.file_manager import FileManager
from src.logger_cfg import logg

"""
data source: https://www.kaggle.com/datasets/buntyshah/auto-insurance-claims-data
"""
class SourceLoader:
    __DATA_FOLDER = "raw"
    __KAGGLE_DATASET_HANDLE = "buntyshah/auto-insurance-claims-data"
    __DATA_FILE_NAME = "insurance_claims.csv"

    def __init__(self):
        self.__file_manager = FileManager()

    def get_insurance_claims_data(self) -> Generator[dict[str, Any], None, None]:
        file_path = self.__download_file()
        for row in self.__read_file(file_path):
            yield row

    def __read_file(self, file_path: Path, chunk_size: int = 100) -> Generator[dict[str, Any], None, None]:
        result = duckdb.sql(f"SELECT * FROM '{file_path}'")
        columns = [desc[0] for desc in result.description]

        for rows in iter(lambda: result.fetchmany(chunk_size), []):
            for row in rows:
                yield dict(zip(columns, row))

    def __download_file(self) -> Path:
        folder_path = self.__file_manager.create_data(SourceLoader.__DATA_FOLDER)
        file_path = folder_path / SourceLoader.__DATA_FILE_NAME

        if file_path.exists():
            logg.info("File already exists, loading from disk...")
        else:
            logg.info("Downloading from Kaggle...")
            kagglehub.dataset_download(
                handle=SourceLoader.__KAGGLE_DATASET_HANDLE,
                output_dir=str(folder_path)
            )

        return file_path
