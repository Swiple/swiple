# Use for local development only
import os
from dotenv import load_dotenv


if __name__ == '__main__':
    # Load environment variables from .env file
    dotenv_path = os.path.join(os.path.dirname(__file__), '../../docker/.env-local')
    load_dotenv(dotenv_path)

    # Start the Celery worker
    from app.worker.app import celery_app
    celery_app.worker_main(['--app', 'app.worker.app.celery_app', 'worker', '-l', 'info', '-c', '4', '-Ofair', '--without-heartbeat', '--without-gossip', '--without-mingle'])
