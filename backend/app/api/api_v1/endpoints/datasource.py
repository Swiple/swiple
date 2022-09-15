from typing import Optional

import sqlalchemy.exc
from fastapi import APIRouter, HTTPException, status, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.exc import DBAPIError
from app.api.shortcuts import get_by_key_or_404
from app.models.datasource import (
	engine_types,
	Datasource,
)
from app.db.client import client
from app.repositories.datasource import DatasourceRepository, get_datasource_repository
from app.repositories.expectation import ExpectationRepository, get_expectation_repository
from app.settings import settings
from app import utils
from opensearchpy import RequestError
from fastapi.param_functions import Depends
import uuid
from app.core.users import current_active_user
from app.models.users import UserDB
from app import constants as c
import requests

router = APIRouter(
	dependencies=[Depends(current_active_user)]
)


@router.get("/json-schema")
def get_json_schema():
	data_sources = []

	for data_source in engine_types.values():
		data_sources.append(data_source.schema())

	return data_sources


@router.get("", response_model=list[Datasource])
def list_datasources(
		sort_by_key: Optional[str] = "datasource_name",
		asc: Optional[bool] = True,
		repository: DatasourceRepository = Depends(get_datasource_repository),
):
	# TODO implement scrolling
	direction = "asc" if asc else "desc"

	try:
		return repository.query(
			{
				"query": {"match_all": {}},
				"sort": [
					{sort_by_key: direction}
				]
			},
			size=1000
		)
	except RequestError:
		raise HTTPException(
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
			detail=f"invalid sort_by_key"
		)


@router.get("/{key}", response_model=Datasource)
def get_datasource(
		key: str,
		repository: DatasourceRepository = Depends(get_datasource_repository),
):
	return get_by_key_or_404(key, repository)


@router.post("", response_model=Datasource)
def create_datasource(
		datasource: Datasource,
		test: Optional[bool] = False,
		user: UserDB = Depends(current_active_user),
		repository: DatasourceRepository = Depends(get_datasource_repository),
):
	try:
		datasource = engine_types[datasource.engine](**datasource.dict(exclude_none=True))
	except KeyError:
		raise HTTPException(
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
			detail=f"datasource {datasource.engine} is not supported"
		)
	except ValidationError as exc:
		return JSONResponse(
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
			content={"detail": exc.errors(), "body": datasource},
		)

	return _create_datasource(datasource, test, user, repository)


@router.put("/{key}", response_model=Datasource)
def update_datasource(
		datasource: Datasource,
		key: str,
		test: Optional[bool] = False,
		repository: DatasourceRepository = Depends(get_datasource_repository),
):
	try:
		datasource = engine_types[datasource.engine](**datasource.dict(exclude_none=True))
	except KeyError:
		raise HTTPException(
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
			detail=f"datasource {datasource.engine} is not supported"
		)
	except ValidationError as exc:
		return JSONResponse(
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
			content={"detail": exc.errors(), "body": datasource},
		)
	return _update_datasource(datasource, key, test, repository)


@router.delete("/{datasource_id}")
def delete_datasource(
		datasource_id: str,
		request: Request,
		repository: DatasourceRepository = Depends(get_datasource_repository),
		expectation_repository: ExpectationRepository = Depends(get_expectation_repository),
):
	return _delete_datasource(datasource_id, request, repository, expectation_repository)


def _test_datasource(datasource: Datasource):
	try:
		engine = create_engine(datasource.connection_string())
		connection = engine.connect()
	except DBAPIError as ex:
		raise HTTPException(
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
			detail=str(ex.orig),
		)
	except sqlalchemy.exc.NoSuchModuleError as ex:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail=str(f"{ex}. This module needs to be installed before it can be used."),
		)
	except ModuleNotFoundError as ex:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail=str(f"{ex}. This module needs to be installed before it can be used."),
		)

	connection.close()
	engine.dispose()

	return JSONResponse(
		status_code=status.HTTP_200_OK,
		content="Successfully connected"
	)


def _delete_datasource(
		key: str,
		request: Request,
		repository: DatasourceRepository,
		expectation_repository: ExpectationRepository,
):
	body = {"query": {"match": {"datasource_id": key}}}
	client.delete_by_query(index=settings.VALIDATION_INDEX, body=body)
	expectation_repository.delete_by_filter(datasource_id=key)
	client.delete_by_query(index=settings.DATASET_INDEX, body=body)
	requests.delete(
		url=f"{settings.SCHEDULER_API_URL}/api/v1/schedules",
		params={"datasource_id": key},
		headers=request.headers,
		cookies=request.cookies,
	)
	repository.delete(key)
	return JSONResponse(
		status_code=status.HTTP_200_OK,
		content="datasource deleted"
	)


def _update_datasource(datasource_update: Datasource, key: str, test: bool, repository: DatasourceRepository):
	original_datasource = get_by_key_or_404(key, repository)

	if original_datasource.datasource_name != datasource_update.datasource_name:
		if len(repository.query_by_name(datasource_update.datasource_name)) > 0:
			raise HTTPException(
				status_code=status.HTTP_409_CONFLICT,
				detail=f"Data Source Name '{datasource_update.datasource_name}' already exists"
			)

	update_dict = {
		**datasource_update.dict(exclude={"create_date", "created_by", "password"}),
		"modified_date": utils.current_time(),
	}
	if hasattr(datasource_update, "password") and datasource_update.password:
		if datasource_update.password.get_decrypted_value() != c.SECRET_MASK:
			update_dict["password"] = datasource_update.password

	if test:
		datasource_for_test = original_datasource.copy(update=update_dict)
		_test_datasource(datasource_for_test)

	updated_datasource = repository.update(key, original_datasource, update_dict)

	# instead of performing a join on datasource_id in the GET /dataset endpoint,
	# we will store the 'datasource_name' and 'database' properties in the
	# dataset document. Updates to 'datasource_name' and 'database' are not common
	# actions while getting the list of datasets is. Using nested docs was considered,
	# but we chose index simplicity over an increase in index load.
	update_by_query_string = ""

	if datasource_update.database != original_datasource.database:
		update_by_query_string += f"ctx._source.database = '{datasource_update.database}';"

	if datasource_update.datasource_name != original_datasource.datasource_name:
		update_by_query_string += f"ctx._source.datasource_name = '{datasource_update.datasource_name}';"

	if update_by_query_string != "":
		client.update_by_query(
			index=settings.DATASET_INDEX,
			body={
				"query": {"match": {"datasource_id": key}},
				"script": {
					"source": update_by_query_string,
					"lang": "painless"
				}
			},
			wait_for_completion=True,
		)

	return updated_datasource


def _create_datasource(datasource: Datasource, test: bool, user: UserDB, repository: DatasourceRepository):
	if test:
		_test_datasource(datasource)

	if len(repository.query_by_name(datasource.datasource_name)) > 0:
		raise HTTPException(
			status_code=status.HTTP_409_CONFLICT,
			detail=f"datasource '{datasource.datasource_name}' already exists"
		)

	datasource.created_by = user.email
	datasource.create_date = utils.current_time()
	datasource.modified_date = utils.current_time()

	return repository.create(str(uuid.uuid4()), datasource)
