from app.db.client import client
from app.settings import settings


VERSION_CONTROL_INDEX = settings.VERSION_CONTROL_INDEX

source_client = client
destination_client = source_client
