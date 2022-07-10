from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse

from app.db.client import client
from app.config.settings import settings
from fastapi.param_functions import Depends
from app.core.users import current_active_user

router = APIRouter(
    dependencies=[Depends(current_active_user)]
)

@router.route("/")
def list_something():
    pass



# POST /datasets/{dataset_id}/suggest
# GET /suggestions
# GET /suggestions/{suggestion_id}
# PUT /suggestions/{suggestion_id}/enable
# PUT /suggestions/{suggestion_id}/disable


# /datasets/{dataset_id}/validate/
# /datasets/{dataset_id}/validate/

