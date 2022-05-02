from fastapi import HTTPException, status
from app.models.base_model import BaseModel
from pydantic import Field
from typing import Optional
from app.config.settings import settings
from app.db.client import client
from app.core import security
from opensearchpy import NotFoundError


ATHENA = "Athena"
POSTGRESQL = "PostgreSQL"
MYSQL = "MySQL"
REDSHIFT = "Redshift"
SNOWFLAKE = "Snowflake"
BIGQUERY = "BigQuery"


class DatasourceCommon(BaseModel):
    key: Optional[str]
    datasource_name: str
    description: str
    created_by: Optional[str]
    create_date: Optional[str]
    modified_date: Optional[str]


class Athena(DatasourceCommon):
    engine: str = Field(ATHENA, const=True)
    database: Optional[str]
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


class PostgreSQL(DatasourceCommon):
    engine: str = Field(POSTGRESQL, const=True)
    username: str
    password: str
    database: str
    host: str
    port: int = Field(placeholder=5432)

    def connection_string(self):
        return f"postgresql+psycopg2://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"

    def expectation_meta(self):
        return {
            "engine": self.engine,
            "database": self.database,
        }


class MySQL(DatasourceCommon):
    engine: str = Field(MYSQL, const=True)
    username: str
    password: str
    database: str
    host: str
    port: int = Field(placeholder=3306)

    def connection_string(self):
        return f"mysql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"

    def expectation_meta(self):
        return {
            "engine": self.engine,
            "database": self.database,
        }


class Redshift(DatasourceCommon):
    engine: str = Field(REDSHIFT, const=True)
    username: str
    password: str
    database: str
    host: str
    port: int = Field(placeholder=5439)
    ssl_mode: str

    def connection_string(self):
        return f"postgresql+psycopg2://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}?sslmode={self.ssl_mode}"

    def expectation_meta(self):
        return {
            "engine": self.engine,
            "database": self.database,
        }


class Snowflake(DatasourceCommon):
    engine: str = Field(SNOWFLAKE, const=True)
    account_name: str
    warehouse: str
    username: str
    password: str
    database: str
    role: str

    def connection_string(self):
        return f"snowflake://{self.username}:{self.password}@{self.account_name}/{self.database}?warehouse={self.warehouse}&role={self.role}"

    def expectation_meta(self):
        return {
            "account_name": self.account_name,
            "warehouse": self.warehouse,
            "engine": self.engine,
            "database": self.database,
        }


# An update to "_update_datasource" update_by_query and Dataset.js breadcrumb for BigQuery to work.
# class BigQuery(DatasourceCommon):
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


def get_datasource(key: str, decrypt_pw: bool = False):
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
    ds_response["_source"]["key"] = ds_response["_id"]
    ds = ds_response["_source"]

    engine = engine_types[ds["engine"]]
    datasource = engine(**ds)

    if hasattr(datasource, "password"):
        if decrypt_pw:
            datasource.password = security.decrypt_password(datasource.password)
        else:
            datasource.password = "*****"
    return datasource


engine_types = {
    ATHENA: Athena,
    POSTGRESQL: PostgreSQL,
    MYSQL: MySQL,
    REDSHIFT: Redshift,
    SNOWFLAKE: Snowflake,
    # BIGQUERY: BigQuery,
}
