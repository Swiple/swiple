from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from fastapi.responses import JSONResponse
from opensearchpy import NotFoundError
from typing import Optional, List

from app.api.shortcuts import get_by_key_or_404
from app.core.users import current_active_user
from app.models.destinations.destination import destinations_map, DestinationUpdate
from app.models.destinations.destination import (
    Destination,
)
from app.models.users import UserDB
from app.repositories.action import ActionRepository, get_action_repository
from app.repositories.destination import DestinationRepository, get_destination_repository
from app.utils import json_schema_to_single_doc, remove_masked_key_value


router = APIRouter(
    dependencies=[Depends(current_active_user)]
)


@router.get("/json-schema")
def get_json_schema():
    destinations = []
    for destination in destinations_map.values():
        json_schema = json_schema_to_single_doc(destination.schema())
        destinations.append(json_schema)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=destinations
    )


@router.get("", response_model=List[Destination])
def list_destinations(
    asc: Optional[bool] = True,
    repository: DestinationRepository = Depends(get_destination_repository),
):
    return repository.list(asc=asc)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_destination(
    destination: Destination,
    user: UserDB = Depends(current_active_user),
    repository: DestinationRepository = Depends(get_destination_repository),
):
    destination.created_by = user.email

    if (repository.count_by_filter(
            destination_name=destination.destination_name,
    ) > 0):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"The destination {destination.destination_name} already exists",
        )

    return repository.create(destination.key, destination)


@router.put("/{key}", response_model=Destination)
def update_destination(
    key: str,
    destination_update: DestinationUpdate,
    repository: DestinationRepository = Depends(get_destination_repository),
    action_repository: ActionRepository = Depends(get_action_repository),
):
    destination = get_by_key_or_404(key, repository)

    if destination_update.destination_name != destination.destination_name:
        if (repository.count_by_filter(
            destination_name=destination_update.destination_name,
        ) > 0):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"The destination '{destination_update.destination_name}' already exists",
            )

    if destination_update.kwargs.destination_type != destination.kwargs.destination_type:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Destination Type cannot be changed once created."
        )

    # remove fields that are EncryptedStr types and have not been updated
    destination_update_as_dict = remove_masked_key_value(destination_update.dict(exclude_none=True))

    # if a destination is associated with any actions, we need to update the actions.
    if action_repository.count_by_filter(
        destination_name=destination.destination_name,
    ) > 0:
        destination_update_as_dict.pop("create_date", None)
        destination_update_as_dict.pop("modified_date", None)

        # restructure fields that need to be updated
        script_source = flatten_dict(destination_update_as_dict)
        action_repository.update_action_by_query(
            key=key,
            script_source=script_source,
            script_params=destination_update_as_dict,
        )

    return repository.update(key, destination, destination_update_as_dict)


@router.delete("/{key}")
def delete_destination(
    key: str,
    repository: DestinationRepository = Depends(get_destination_repository),
    action_repository: ActionRepository = Depends(get_action_repository),
):
    try:
        action_repository.delete_by_query({"query": {"match": {"destination.key": key}}})
        repository.delete(key)
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Destination with id '{key}' does not exist"
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="Destination deleted"
    )


@router.get("/{key}", response_model=Destination)
def get_destination(
    key: str,
    repository: DestinationRepository = Depends(get_destination_repository),
):
    return repository.get(key)


def flatten_dict(d, sep="."):
    obj = {}

    def traverse(t, parent_key=""):
        if isinstance(t, dict):
            for k, v in t.items():
                traverse(v, parent_key + sep + k if parent_key else k)
        elif isinstance(t, (str, bool, int, float)):
            obj[parent_key] = t
        else:
            raise NotImplementedError(f't is of type, {type(t)}, which is not an approved type.')

    def to_update_script(flattened_dict):
        flattened_string = ""
        for key, value in flattened_dict.items():
            flattened_string += f"ctx._source.destination.{key} = params.{key};\n"
        return flattened_string

    traverse(d)
    flattened = to_update_script(obj)
    return flattened
