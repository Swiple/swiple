from fastapi import APIRouter, status, HTTPException
from fastapi.param_functions import Depends
from fastapi.responses import JSONResponse
import sqlalchemy as sa
from sqlalchemy.exc import DBAPIError

from app.api.shortcuts import get_by_key_or_404
from app.core.users import current_active_user
from app.repositories.datasource import DatasourceRepository, get_datasource_repository

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
            status_code=status.HTTP_400_BAD_REQUEST,
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

    engine = sa.create_engine(datasource.connection_string())
    inspect = sa.inspect(engine)
    schema_list = inspect.get_table_names(schema=schema)

    return JSONResponse(status_code=status.HTTP_200_OK, content=schema_list)


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
