from typing import Any, Generator

from sqlalchemy import create_engine, MetaData, Table, text, inspect, UniqueConstraint
from sqlalchemy.dialects.postgresql import insert

from src.settings import Settings

class ClaimRepository:
    __silver = "claims_silver"
    __gold = "claims_gold"

    def __init__(self):
        self.__engine = create_engine(Settings().db_connection_uri())
        self.__metadata = MetaData()

    def save_claims_silver(self, data: list[dict[str, Any]]) -> None:
        self.__save(self.__silver, data, ["policy_number", "incident_date"])

    def save_claims_gold(self, data: list[dict[str, Any]]) -> None:
        self.__save(self.__gold, data, ["policy_number", "incident_date"])

    def load_claims_silver(self) -> Generator[dict[str, Any], None, None]:
        return self.__load(self.__silver)

    def __save(self, table_name: str, data: list[dict[str, Any]], key_columns: list[str]):
        if not data:
            return

        self.__create_table_if_not_exists(table_name, data[0], key_columns)
        table = Table(table_name, self.__metadata, autoload_with=self.__engine)
        statement = insert(table).values(data)

        update_dict = dict()
        for column in table.columns:
            if column.name not in key_columns:
                update_dict[column.name] = statement.excluded[column.name]
        upsert_statement = statement.on_conflict_do_update(index_elements=key_columns, set_=update_dict)

        with self.__engine.begin() as conn:
            conn.execute(upsert_statement)

    def __load(self, table_name: str, chunksize: int = 100) -> Generator[dict[str, Any], None, None]:
        query = f"SELECT * FROM {table_name}"
        with self.__engine.connect() as conn:
            result = conn.execute(text(query))

            while True:
                rows = result.fetchmany(chunksize)
                if not rows:
                    break

                for row in rows:
                    yield dict(row._mapping)

    def __create_table_if_not_exists(self, table_name: str, sample_row: dict[str, Any], key_columns: list[str]):
        inspector = inspect(self.__engine)
        if inspector.has_table(table_name):
            return

        columns = self.__infer_columns(sample_row)
        unique_constraint = UniqueConstraint(*key_columns, name=f"{table_name}_unique")
        table = Table(table_name, self.__metadata, *columns, unique_constraint)
        table.create(self.__engine)

    def __infer_columns(self, sample_row: dict[str, Any]) -> list[Any]:
        from sqlalchemy import Column, String, Integer, Float, Boolean

        type_map = {
            int: Integer,
            float: Float,
            bool: Boolean,
            str: String,
        }

        columns = []
        for name, value in sample_row.items():
            col_type = type_map.get(type(value), String)
            columns.append(Column(name, col_type()))

        return columns
