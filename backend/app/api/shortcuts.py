from fastapi import HTTPException, status

from app.repositories.base import BaseRepository, M, NotFoundError


def get_by_key_or_404(key: str, repository: BaseRepository[M]) -> M:
    try:
        return repository.get(key)
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{repository.model_class.__name__} with id '{key}' does not exist"
        )


def delete_by_key_or_404(key: str, repository: BaseRepository[M]) -> None:
    try:
        repository.delete(key)
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{repository.model_class.__name__} with id '{key}' does not exist"
        )
