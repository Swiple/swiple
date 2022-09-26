from typing import Optional

from fastapi import APIRouter
from app.models.validation import Validation, Stats
from app.repositories.validation import ValidationRepository, get_validation_repository
from fastapi.param_functions import Depends
from app.core.users import current_active_user

router = APIRouter(
    dependencies=[Depends(current_active_user)]
)


@router.get("", response_model=list[Validation])
def list_validations(
        datasource_id: Optional[str] = None,
        dataset_id: Optional[str] = None,
        repository: ValidationRepository = Depends(get_validation_repository),
):
    return repository.query_by_filter(
        datasource_id=datasource_id,
        dataset_id=dataset_id,
    )


@router.get("/statistics", response_model=Stats)
def validations(
        dataset_id: str,
        repository: ValidationRepository = Depends(get_validation_repository),

):
    statistics = repository.statistics(
        dataset_id=dataset_id,
    )

    aggs = statistics["aggregations"]

    validations_dataset = []
    for daily_bucket in aggs["validation_counts"]["buckets"]:
        objective_pass_rate = daily_bucket["1_day"]["value"]
        validations_dataset.append([daily_bucket["key_as_string"], objective_pass_rate])

    return Stats(
        **{
            "1_day_avg": aggs["1_day"]["success_counts"]["value"],
            "7_day_avg": aggs["7_day"]["success_counts"]["value"],
            "31_day_avg": aggs["31_day"]["success_counts"]["value"],
            "validations": validations_dataset,
        }
    )
