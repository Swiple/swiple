from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
import sqlalchemy as sa
from sqlalchemy.exc import DBAPIError

from app.models.datasource import get_datasource
from fastapi.param_functions import Depends
from app.core.users import current_active_user

router = APIRouter(
    dependencies=[Depends(current_active_user)]
)


@router.get("/schema")
def list_schemas(datasource_id: str):
    datasource = get_datasource(key=datasource_id)
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
def list_tables(datasource_id: str, schema: str):
    datasource = get_datasource(key=datasource_id)

    engine = sa.create_engine(datasource.connection_string())
    inspect = sa.inspect(engine)
    schema_list = inspect.get_table_names(schema=schema)

    return JSONResponse(status_code=status.HTTP_200_OK, content=schema_list)


@router.get("/column")
def list_columns(datasource_id: str, schema: str, table: str):
    datasource = get_datasource(key=datasource_id)
    engine = sa.create_engine(datasource.connection_string())
    inspect = sa.inspect(engine)
    sa_column_list = inspect.get_columns(schema=schema, table_name=table)

    column_list = []

    for column in sa_column_list:
        column_list.append({"name": column["name"], "type": str(column["type"])})

    return JSONResponse(status_code=status.HTTP_200_OK, content=column_list)
