from fastapi import APIRouter, status, HTTPException
from fastapi.param_functions import Depends
from fastapi.responses import JSONResponse
import sqlalchemy as sa
from sqlalchemy.exc import DBAPIError

from app.api.shortcuts import get_by_key_or_404
from app.core.users import current_active_user
from app.repositories.datasource import DatasourceRepository, get_datasource_repository
from app.models.datasource import Engine

from great_expectations.execution_engine import SqlAlchemyExecutionEngine
from great_expectations.datasource.data_connector import (
    InferredAssetSqlDataConnector,
)


router = APIRouter(
    dependencies=[Depends(current_active_user)]
)


@router.get("/schema")
def list_schemas(
    datasource_id: str,
    datasource_repository: DatasourceRepository = Depends(get_datasource_repository),
):
    datasource = get_by_key_or_404(datasource_id, datasource_repository)
    try:
        engine = sa.create_engine(datasource.connection_string())
        inspect = sa.inspect(engine)
        schema_list = inspect.get_schema_names()
    except DBAPIError as ex:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(ex),
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content=schema_list)


@router.get("/table")
def list_tables(
    datasource_id: str,
    schema: str,
    datasource_repository: DatasourceRepository = Depends(get_datasource_repository),
):
    datasource = get_by_key_or_404(datasource_id, datasource_repository)

    execution_engine = SqlAlchemyExecutionEngine(
        connection_string=datasource.connection_string(),
    )
    connector: InferredAssetSqlDataConnector = InferredAssetSqlDataConnector(
        name=datasource.datasource_name,
        datasource_name=datasource.datasource_name,
        execution_engine=execution_engine,
        introspection_directives={
            "schema_name": schema,
            "ignore_information_schemas_and_system_tables": False,
            "include_views": True,
        },
    )
    tables = connector.get_available_data_asset_names_and_types()

    if datasource.engine == Engine.BIGQUERY:
        tables = [(table.split(".")[1], table_type) for table, table_type in tables]

    return JSONResponse(status_code=status.HTTP_200_OK, content=tables)


@router.get("/column")
def list_columns(
    datasource_id: str,
    schema: str,
    table: str,
    datasource_repository: DatasourceRepository = Depends(get_datasource_repository),
):
    datasource = get_by_key_or_404(datasource_id, datasource_repository)
    engine = sa.create_engine(datasource.connection_string())
    inspect = sa.inspect(engine)
    sa_column_list = inspect.get_columns(schema=schema, table_name=table)

    column_list = []

    for column in sa_column_list:
        column_list.append({"name": column["name"], "type": str(column["type"])})

    return JSONResponse(status_code=status.HTTP_200_OK, content=column_list)
