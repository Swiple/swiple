from enum import Enum
from typing import Annotated, Optional, Literal, Union

from pydantic import Field

from app.models.base_model import BaseModel, CreateUpdateDateModel, KeyModel
from app.models.types import EncryptedStr


class Engine(str, Enum):
    ATHENA = "Athena"
    POSTGRESQL = "PostgreSQL"
    MYSQL = "MySQL"
    REDSHIFT = "Redshift"
    SNOWFLAKE = "Snowflake"
    BIGQUERY = "BigQuery"
    TRINO = "Trino"


class DatasourceBase(BaseModel, KeyModel, CreateUpdateDateModel):
    engine: Engine
    datasource_name: str
    description: Optional[str]
    created_by: Optional[str]

    def connection_string(self):
        """Returns a SQLAlchemy compatible connection string."""
        pass

    def expectation_meta(self):
        """Returns connection metadata to be included in validation."""
        pass


class Athena(DatasourceBase):
    engine: Literal[Engine.ATHENA]
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


class PostgreSQL(DatasourceBase):
    engine: Literal[Engine.POSTGRESQL]
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


class MySQL(DatasourceBase):
    engine: Literal[Engine.MYSQL]
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


class Redshift(DatasourceBase):
    engine: Literal[Engine.REDSHIFT]
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


class Snowflake(DatasourceBase):
    engine: Literal[Engine.SNOWFLAKE]
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


class Trino(DatasourceBase):
    engine: Literal[Engine.TRINO]
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
class BigQuery(DatasourceBase):
    engine: Literal[Engine.BIGQUERY]
    database: str = Field(title="GCP Project")
    credentials_info: Optional[EncryptedStr] = Field(
        placeholder='{ "credentials_info": {"type": "service_account", "project_id": "...", "private_key_id": "...", "private_key": "...", "client_email": "...", "client_id": "...", "auth_uri": "...", "token_uri": "...", "auth_provider_x509_cert_url": "...", "client_x509_cert_url": "..."}}',
    )

    def connection_string(self, dataset=None):
        connection = f"bigquery://{self.database}"
        if dataset is not None:
            connection = f"{connection}/{dataset}"
        if self.credentials_info:
            connection = f"{connection}?credentials_info={self.credentials_info}"
        return connection

    def expectation_meta(self):
        return {
            "engine": self.engine,
            "database": self.database,
        }


Datasource = Union[
    Athena,
    BigQuery,
    PostgreSQL,
    MySQL,
    Redshift,
    Snowflake,
    Trino,
]


class DatasourceInput(BaseModel):
    __root__: Annotated[Datasource, Field(discriminator="engine")]
