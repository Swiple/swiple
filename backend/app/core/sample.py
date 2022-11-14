import datetime
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError, OperationalError

from app.models.dataset import BaseDataset, Sample
from app.models.datasource import Datasource
from app.utils import add_limit_clause


class GetSampleException(Exception):
    def __init__(self, error: Any, *args: object) -> None:
        self.error = error
        super().__init__(*args)


def get_dataset_sample(dataset: BaseDataset, datasource: Datasource) -> Sample:
    if dataset.runtime_parameters:
        return get_sample_query_results(
            query=dataset.runtime_parameters.query,
            url=datasource.connection_string()
        )

    return get_sample_query_results(
        query=f"select * from {dataset.dataset_name}",
        url=datasource.connection_string(),
    )


def get_sample_query_results(query: str, url: str) -> Sample:
    try:
        query = add_limit_clause(query)

        with create_engine(url).connect() as con:
            execution = con.execute(query)
            # TODO neaten up
            result_set = []
            columns, rows = get_columns_and_rows(execution)

            for i, row in enumerate(rows):
                temp_row = {"key": i}
                row = list(row)

                for key in columns:
                    for value in row:
                        if isinstance(value, datetime.datetime):
                            temp_row[key] = value.__str__()
                        else:
                            temp_row[key] = value

                        row.remove(value)
                        break

                result_set.append(temp_row)

            if len(columns) == 0:
                raise GetSampleException("No columns included in statement.")
            return Sample(columns=columns, rows=result_set)
    except ProgrammingError as e:
        raise GetSampleException(e.orig.pgerror) from e
    except OperationalError as e:
        raise GetSampleException(e.orig) from e


def get_columns_and_rows(execution):
    return list(execution.keys()), execution.all()
