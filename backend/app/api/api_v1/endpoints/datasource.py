from typing import Optional

import sqlalchemy.exc
from fastapi import APIRouter, HTTPException, status, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.exc import DBAPIError
from app.api.shortcuts import get_by_key_or_404
from app.models.datasource import (
	DatasourceCreate,
	DatasourceUpdate,
	engine_types,
	Datasource,
)
from app.db.client import client
from app.repositories.dataset import DatasetRepository, get_dataset_repository
from app.repositories.datasource import DatasourceRepository, get_datasource_repository
from app.repositories.expectation import ExpectationRepository, get_expectation_repository
from app.settings import settings
from app import utils
from opensearchpy import RequestError
from fastapi.param_functions import Depends
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


@router.get("")
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


@router.get("/{key}")
def get_datasource(
		key: str,
		repository: DatasourceRepository = Depends(get_datasource_repository),
):
	return get_by_key_or_404(key, repository)


@router.post("")
def create_datasource(
		datasource_create: DatasourceCreate,
		test: Optional[bool] = False,
		user: UserDB = Depends(current_active_user),
		repository: DatasourceRepository = Depends(get_datasource_repository),
):
	try:
		datasource = engine_types[datasource_create.engine](
			**datasource_create.dict(),
			created_by=user.email,
		)
	except KeyError:
		raise HTTPException(
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
			detail=f"datasource {datasource_create.engine} is not supported"
		)
	except ValidationError as exc:
		return JSONResponse(
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
			content={"detail": exc.errors(), "body": datasource_create},
		)

	return _create_datasource(datasource, test, repository)


@router.put("/{key}")
def update_datasource(
		key: str,
		datasource_update: DatasourceUpdate,
		test: Optional[bool] = False,
		user: UserDB = Depends(current_active_user),
		repository: DatasourceRepository = Depends(get_datasource_repository),
		dataset_repository: DatasetRepository = Depends(get_dataset_repository),
):
	try:
		datasource = engine_types[datasource_update.engine](
			**datasource_update.dict(),
			created_by=user.email,
		)
	except KeyError:
		raise HTTPException(
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
			detail=f"datasource {datasource_update.engine} is not supported"
		)
	except ValidationError as exc:
		return JSONResponse(
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
			content={"detail": exc.errors(), "body": datasource_update},
		)
	return _update_datasource(datasource, key, test, repository, dataset_repository)


@router.delete("/{datasource_id}")
def delete_datasource(
		datasource_id: str,
		request: Request,
		repository: DatasourceRepository = Depends(get_datasource_repository),
		dataset_repository: DatasetRepository = Depends(get_dataset_repository),
		expectation_repository: ExpectationRepository = Depends(get_expectation_repository),
):
	return _delete_datasource(datasource_id, request, repository, dataset_repository, expectation_repository)


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
		dataset_repository: DatasetRepository,
		expectation_repository: ExpectationRepository,
):
	body = {"query": {"match": {"datasource_id": key}}}
	client.delete_by_query(index=settings.VALIDATION_INDEX, body=body)
	expectation_repository.delete_by_datasource(key)
	dataset_repository.delete_by_datasource(key)
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


def _update_datasource(datasource_update: Datasource, key: str, test: bool, repository: DatasourceRepository, dataset_repository: DatasetRepository):
	original_datasource = get_by_key_or_404(key, repository)

	if original_datasource.datasource_name != datasource_update.datasource_name:
		if len(repository.query_by_name(datasource_update.datasource_name)) > 0:
			raise HTTPException(
				status_code=status.HTTP_409_CONFLICT,
				detail=f"Data Source Name '{datasource_update.datasource_name}' already exists"
			)

	update_dict = datasource_update.dict(exclude={"create_date", "created_by", "password"})
	if hasattr(datasource_update, "password") and datasource_update.password:
		if datasource_update.password.get_decrypted_value() != c.SECRET_MASK:
			update_dict["password"] = datasource_update.password

	if test:
		datasource_for_test = original_datasource.copy(update=update_dict)
		_test_datasource(datasource_for_test)

	updated_datasource = repository.update(key, original_datasource, update_dict)

	updated_database = datasource_update.database if datasource_update.database != original_datasource.database else None
	updated_datasource_name = datasource_update.datasource_name if datasource_update.datasource_name != original_datasource.datasource_name else None
	dataset_repository.update_datasource(key, database=updated_database, datasource_name=updated_datasource_name)

	return updated_datasource


def _create_datasource(datasource: Datasource, test: bool, repository: DatasourceRepository):
	if test:
		_test_datasource(datasource)

	if len(repository.query_by_name(datasource.datasource_name)) > 0:
		raise HTTPException(
			status_code=status.HTTP_409_CONFLICT,
			detail=f"datasource '{datasource.datasource_name}' already exists"
		)

	return repository.create(datasource.key, datasource)
