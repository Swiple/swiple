from copy import deepcopy

import sqlalchemy.exc
from fastapi import APIRouter, HTTPException, status, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.exc import DBAPIError
from app.models.datasource import (
	engine_types,
	Datasource,
)
from app.db.client import client
from app.settings import settings
from app import utils
from typing import Optional
from opensearchpy import RequestError
from app.models import datasource as datasourcee
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

	return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(data_sources))


@router.get("")
def list_datasources(
		sort_by_key: Optional[str] = "datasource_name",
		asc: Optional[bool] = True,
):
	# TODO implement scrolling
	direction = "asc" if asc else "desc"

	try:
		docs = client.search(
			index=settings.DATASOURCE_INDEX,
			size=1000,
			body={
				"query": {"match_all": {}},
				"sort": [
					{sort_by_key: direction}
				]
			}
		)["hits"]["hits"]
	except RequestError:
		raise HTTPException(
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
			detail=f"invalid sort_by_key"
		)

	docs_response = []
	for doc in docs:
		if doc["_source"].get("password"):
			doc["_source"]["password"] = c.SECRET_MASK

		doc["_source"]["key"] = doc["_id"]
		docs_response.append(
			dict(**doc["_source"])
		)
	return JSONResponse(status_code=status.HTTP_200_OK, content=docs_response)


@router.get("/{key}")
def get_datasource(
		key: str,
):
	doc = datasourcee.get_datasource(key=key).dict(by_alias=True)
	return JSONResponse(status_code=status.HTTP_200_OK, content=doc)


@router.post("")
def create_datasource(
		datasource: Datasource,
		test: Optional[bool] = False,
		user: UserDB = Depends(current_active_user),
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
			content=jsonable_encoder({"detail": exc.errors(), "body": datasource}),
		)

	return _create_datasource(datasource, test, user)


@router.put("/{key}")
def update_datasource(
		datasource: Datasource,
		key: str,
		test: Optional[bool] = False,
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
			content=jsonable_encoder({"detail": exc.errors(), "body": datasource}),
		)
	return _update_datasource(datasource, key, test)


@router.delete("/{datasource_id}")
def delete_datasource(
		datasource_id: str,
		request: Request,
):
	return _delete_datasource(datasource_id, request)


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
):
	body = {"query": {"match": {"datasource_id": key}}}
	client.delete_by_query(index=settings.VALIDATION_INDEX, body=body)
	client.delete_by_query(index=settings.EXPECTATION_INDEX, body=body)
	client.delete_by_query(index=settings.DATASET_INDEX, body=body)
	requests.delete(
		url=f"{settings.SCHEDULER_API_URL}/api/v1/schedules",
		params={"datasource_id": key},
		headers=request.headers,
		cookies=request.cookies,
	)
	client.delete(index=settings.DATASOURCE_INDEX, id=key, refresh="wait_for")
	return JSONResponse(
		status_code=status.HTTP_200_OK,
		content="datasource deleted"
	)


def _update_datasource(datasource, key: str, test: bool):
	original_datasource = datasourcee.get_datasource(key=key)

	if original_datasource.datasource_name != datasource.datasource_name:
		response = client.search(
			index=settings.DATASOURCE_INDEX,
			body={"query": {"match": {"datasource_name.keyword": datasource.datasource_name}}}
		)

		if response["hits"]["total"]["value"] > 0:
			raise HTTPException(
				status_code=status.HTTP_409_CONFLICT,
				detail=f"Data Source Name '{datasource.datasource_name}' already exists"
			)
	datasource.modified_date = utils.current_time()
	datasource.create_date = original_datasource.create_date
	datasource.created_by = original_datasource.created_by
	datasource_as_dict = datasource.dict(by_alias=True, exclude_none=True)
	if test:
		datasource_for_test = deepcopy(datasource)

		if hasattr(datasource, "password") and datasource.password:
			if datasource.password.get_decrypted_value() == c.SECRET_MASK:
				# password hasn't changed, get it from existing datasource and decrypt password
				datasource_for_test.password = original_datasource.password

				# remove password so we don't update OpenSearch with *****
				datasource_as_dict.pop("password")

		_test_datasource(datasource_for_test)

	client.update(
		index=settings.DATASOURCE_INDEX,
		id=key,
		body={"doc": datasource_as_dict},
		refresh="wait_for",
	)

	datasource_as_dict["key"] = key
	datasource_as_dict["password"] = c.SECRET_MASK

	# instead of performing a join on datasource_id in the GET /dataset endpoint,
	# we will store the 'datasource_name' and 'database' properties in the
	# dataset document. Updates to 'datasource_name' and 'database' are not common
	# actions while getting the list of datasets is. Using nested docs was considered,
	# but we chose index simplicity over an increase in index load.
	update_by_query_string = ""

	if datasource.database != original_datasource.database:
		update_by_query_string += f"ctx._source.database = '{datasource.database}';"

	if datasource.datasource_name != original_datasource.datasource_name:
		update_by_query_string += f"ctx._source.datasource_name = '{datasource.datasource_name}';"

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
	return JSONResponse(
		status_code=status.HTTP_200_OK,
		content=datasource_as_dict
	)


def _create_datasource(datasource, test: bool, user: UserDB):
	if test:
		_test_datasource(datasource)

	response = client.search(
		index=settings.DATASOURCE_INDEX,
		body={"query": {"match": {"datasource_name.keyword": datasource.datasource_name}}}
	)

	if response["hits"]["total"]["value"] > 0:
		raise HTTPException(
			status_code=status.HTTP_409_CONFLICT,
			detail=f"datasource '{datasource.datasource_name}' already exists"
		)

	datasource.created_by = user.email
	datasource.create_date = utils.current_time()
	datasource.modified_date = utils.current_time()

	datasource_as_dict = datasource.dict(by_alias=True, exclude_none=True)

	insert_response = client.index(
		index=settings.DATASOURCE_INDEX,
		id=str(uuid.uuid4()),
		body=datasource_as_dict,
		refresh="wait_for",
	)

	datasource_as_dict["key"] = insert_response["_id"]
	datasource_as_dict["password"] = c.SECRET_MASK

	return JSONResponse(
		status_code=status.HTTP_200_OK,
		content=datasource_as_dict
	)
