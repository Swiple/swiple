from app.core.runner import create_dataset_suggestions
from app.repositories.expectation import ExpectationRepository
from app.db.client import client
from app.worker.app import celery_app


@celery_app.task(name="suggestions.run",)
def run_suggestions(dataset_id):
    results = create_dataset_suggestions(dataset_id)
    expectation_repository = ExpectationRepository(client)
    expectations = [expectation_repository._get_object_from_dict(e) for e in results]
    expectation_repository.delete_by_filter(
        dataset_id=dataset_id,
        suggested=True,
        enabled=False,
    )
    expectation_repository.bulk_create(expectations)
