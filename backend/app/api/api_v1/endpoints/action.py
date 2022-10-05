from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.params import Depends
from fastapi.responses import JSONResponse
from pydantic.error_wrappers import ValidationError
from typing import Optional, List

from app.core.users import current_active_user
from app.models.action import Action, ActionCreateOrUpdate
from app.models.destinations.destination import destination_details_map, DestinationAction
from app.models.users import UserDB
from app.repositories.action import ActionRepository, get_action_repository
from app.repositories.destination import DestinationRepository, get_destination_repository
from app.utils import json_schema_to_single_doc


router = APIRouter(
    dependencies=[Depends(current_active_user)]
)


@router.get("/json-schema")
def get_json_schema():
    destinations = []
    for destination_details in destination_details_map.values():
        json_schema = json_schema_to_single_doc(destination_details.schema())
        destinations.append(json_schema)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=destinations
    )


@router.get("", response_model=List[Action])
def list_actions(
    resource_key: Optional[str] = None,
    action_type: Optional[str] = None,
    destination_name: Optional[str] = None,
    asc: Optional[bool] = True,
    repository: ActionRepository = Depends(get_action_repository),
):
    return repository.list(
        resource_key=resource_key,
        action_type=action_type,
        destination_name=destination_name,
        asc=asc,
    )


@router.post("", response_model=Action, status_code=status.HTTP_201_CREATED)
def create_action(
    action_request: ActionCreateOrUpdate,
    user: UserDB = Depends(current_active_user),
    repository: ActionRepository = Depends(get_action_repository),
    destination_repository: DestinationRepository = Depends(get_destination_repository),
):
    destinations = destination_repository.query_by_name(
        destination_name=action_request.destination.destination_name,
    )

    if len(destinations) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"destination '{action_request.destination.destination_name}' does not exist"
        )

    destination = destinations[0]

    # Combine destination and destination_details kwargs
    destination_kwargs = destination.kwargs.dict()
    destination_details_kwargs = action_request.destination.kwargs.dict()
    action_kwargs = destination_kwargs | destination_details_kwargs

    destination_action = DestinationAction(
        key=destination.key,
        destination_name=action_request.destination.destination_name,
        kwargs=action_kwargs,
    )

    try:
        action = Action(
            resource_key=action_request.resource_key,
            resource_type=action_request.resource_type,
            action_type=action_request.action_type,
            destination=destination_action,
            created_by=user.email,
        )
    except ValidationError as exc:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({"detail": exc.errors()}),
        )

    return repository.create(action.key, action)


@router.put("/{key}", response_model=Action)
def update_action(
    action_request: ActionCreateOrUpdate,
    key: str,
    user: UserDB = Depends(current_active_user),
    repository: ActionRepository = Depends(get_action_repository),
    destination_repository: DestinationRepository = Depends(get_destination_repository),
):
    destinations = destination_repository.query_by_name(
        destination_name=action_request.destination.destination_name,
    )

    if len(destinations) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"destination '{action_request.destination.destination_name}' does not exist"
        )

    destination = destinations[0]

    # Combine destination and destination_details kwargs
    destination_kwargs = destination.kwargs.dict()
    destination_details_kwargs = action_request.destination.kwargs.dict()
    action_kwargs = destination_kwargs | destination_details_kwargs

    destination_action = DestinationAction(
        key=destination.key,
        destination_name=action_request.destination.destination_name,
        kwargs=action_kwargs,
    )

    try:
        action = Action(
            key=key,
            resource_key=action_request.resource_key,
            resource_type=action_request.resource_type,
            action_type=action_request.action_type,
            destination=destination_action,
            created_by=user.email,
        )
    except ValidationError as exc:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({"detail": exc.errors()}),
        )

    return repository.update(key, action, action.dict())


@router.delete("/{key}", responses={200: {"description": "Action deleted"}})
def delete_action(
    key: str,
    repository: ActionRepository = Depends(get_action_repository),
):
    repository.delete(key)
    return "Action deleted"


@router.get("/{key}", response_model=Action)
def get_action(
    key: str,
    repository: ActionRepository = Depends(get_action_repository),
):
    return repository.get(key)

