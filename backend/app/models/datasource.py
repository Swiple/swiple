from fastapi import HTTPException, status
from app.models.base_model import BaseModel
from pydantic import Field, Extra
from typing import Any, Dict, Optional, Literal, Type, TypeVar
from app.settings import settings
from app.db.client import client
from app.models.types import EncryptedStr
from opensearchpy import NotFoundError


ATHENA = "Athena"
POSTGRESQL = "PostgreSQL"
MYSQL = "MySQL"
REDSHIFT = "Redshift"
SNOWFLAKE = "Snowflake"
BIGQUERY = "BigQuery"
TRINO = "Trino"

Engines = Literal[ATHENA, POSTGRESQL, MYSQL, REDSHIFT, SNOWFLAKE, TRINO]


class Datasource(BaseModel):
    class Config:
        extra = Extra.allow

    key: Optional[str]
    engine: Engines
    datasource_name: str
    description: Optional[str]
    created_by: Optional[str]
    create_date: Optional[str]
    modified_date: Optional[str]

    def connection_string(self):
        """Returns a SQLAlchemy compatible connection string."""
        pass

    def expectation_meta(self):
        """Returns connection metadata to be included in validation."""
        pass


D = TypeVar("D", bound=Datasource)


class Athena(Datasource):
    engine: str = Field(ATHENA, const=True)
    database: str
    region: str = Field(placeholder="us-east-1", description="AWS Region")
    s3_staging_dir: str = Field(regex="^s3://", placeholder="s3://YOUR_S3_BUCKET/path/to/", description="Navigate to 'Athena' in the AWS Console then select 'Settings' to find the 'Query result location'.")

    def connection_string(self):
        if self.database:
            return f"awsathena+rest://@athena.{self.region}.amazonaws.com/{self.database}?s3_staging_dir={self.s3_staging_dir}"
        else:
            return f"awsathena+rest://@athena.{self.region}.amazonaws.com/?s3_staging_dir={self.s3_staging_dir}"

    def expectation_meta(self):
        return {
            "engine": self.engine,
            "database": self.database,
            "region": self.region,
            "s3_staging_dir": self.s3_staging_dir,
        }


class PostgreSQL(Datasource):
    engine: str = Field(POSTGRESQL, const=True)
    username: str
    password: EncryptedStr
    database: str
    host: str
    port: int = Field(placeholder=5432)

    def connection_string(self):
        return f"postgresql+psycopg2://{self.username}:{self.password.get_decrypted_value()}@{self.host}:{self.port}/{self.database}"

    def expectation_meta(self):
        return {
            "engine": self.engine,
            "database": self.database,
        }


class MySQL(Datasource):
    engine: str = Field(MYSQL, const=True)
    username: str
    password: EncryptedStr
    database: str
    host: str
    port: int = Field(placeholder=3306)

    def connection_string(self):
        return f"mysql+pymysql://{self.username}:{self.password.get_decrypted_value()}@{self.host}:{self.port}/{self.database}"

    def expectation_meta(self):
        return {
            "engine": self.engine,
            "database": self.database,
        }


class Redshift(Datasource):
    engine: str = Field(REDSHIFT, const=True)
    username: str
    password: EncryptedStr
    database: str
    host: str
    port: int = Field(placeholder=5439)

    def connection_string(self):
        return f"postgresql+psycopg2://{self.username}:{self.password.get_decrypted_value()}@{self.host}:{self.port}/{self.database}"

    def expectation_meta(self):
        return {
            "engine": self.engine,
            "database": self.database,
        }


class Snowflake(Datasource):
    engine: str = Field(SNOWFLAKE, const=True)
    account: str
    user: str
    password: EncryptedStr
    database: str
    warehouse: Optional[str]
    role: Optional[str]

    def connection_string(self, schema=None):
        connection = f"snowflake://{self.user}:{self.password.get_decrypted_value()}@{self.account}/{self.database}"

        if schema:
            connection = f"{connection}/{schema}"

        if self.warehouse:
            connection = f"{connection}?warehouse={self.warehouse}"

        if self.role and self.warehouse:
            connection = f"{connection}&role={self.role}"

        if self.role and not self.warehouse:
            connection = f"{connection}?role={self.role}"

        if not self.role and not self.warehouse:
            return f"{connection}?application=swiple"

        return f"{connection}&application=swiple"

    def expectation_meta(self):
        return {
            "account": self.account,
            "warehouse": self.warehouse,
            "engine": self.engine,
            "database": self.database,
        }


class Trino(Datasource):
    engine: str = Field(TRINO, const=True)
    username: str
    password: Optional[EncryptedStr]
    host: str
    database: str
    port: int = Field(placeholder=8080)
    connection_args: Optional[str] = Field(
        placeholder='These values are not encrypted',
        description='Add additional connection arguments e.g. session_properties={"query_max_run_time": "1d"}&client_tags=["tag1", "tag2"]'
    )

    def connection_string(self):
        url = f'trino://{self.username}:{self.password.get_decrypted_value() if self.password else ""}@{self.host}:{self.port}/{self.database}'
        if self.connection_args and self.connection_args.startswith("?"):
            url += self.connection_args
        if self.connection_args and not self.connection_args.startswith("?"):
            url += "?" + self.connection_args
        return url

    def expectation_meta(self):
        return {
            "engine": self.engine,
            "database": self.database,
        }


# An update to "_update_datasource" update_by_query and Dataset.js breadcrumb for BigQuery to work.
# class BigQuery(Datasource):
#     engine: str = Field(BIGQUERY, const=True)
#     gcp_project: str = Field(title="GCP Project")
#     dataset: str
#
#     def connection_string(self):
#         return f"bigquery://{self.gcp_project}/{self.dataset}"
#
#     def expectation_meta(self):
#         return {
#             "engine": self.engine,
#             "gcp_project": self.gcp_project,
#             "dataset": self.dataset,
#         }

def datasource_from_dict(key: str, data: Dict[str, Any]) -> D:
    engine_class = engine_types[data["engine"]]
    data.pop("key", None)
    return engine_class(key=key, **data)

def get_datasource(key: str):
    try:
        ds_response = client.get(
            index=settings.DATASOURCE_INDEX,
            id=key
        )
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"datasource with id '{key}' does not exist"
        )

    return datasource_from_dict(ds_response["_id"],  ds_response["_source"])


engine_types: Dict[str, Type[D]] = {
    ATHENA: Athena,
    POSTGRESQL: PostgreSQL,
    MYSQL: MySQL,
    REDSHIFT: Redshift,
    SNOWFLAKE: Snowflake,
    TRINO: Trino,
}
