import base64
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
    role_arn: Optional[str] = Field(
        placeholder="arn:aws:iam::<YOUR_ACCOUNT_ID>:role/<YOUR_ROLE_NAME>",
        description="The Amazon Resource Name (ARN) of the AWS Identity and Access Management (IAM) role that Athena uses to access your data on your behalf."
    )
    region: str = Field(placeholder="us-east-1", description="AWS Region")
    s3_staging_dir: str = Field(regex="^s3://", placeholder="s3://YOUR_S3_BUCKET/path/to/", description="Navigate to 'Athena' in the AWS Console then select 'Settings' to find the 'Query result location'.")

    def connection_string(self):
        base_url = f"awsathena+rest://@athena.{self.region}.amazonaws.com/"
        params = {
            "s3_staging_dir": self.s3_staging_dir,
            "role_arn": self.role_arn,
        }
        if self.database:
            base_url += self.database

        query_string = "&".join([f"{k}={v}" for k, v in params.items() if v])
        return f"{base_url}?{query_string}"

    def expectation_meta(self):
        return {
            "engine": self.engine,
            "database": self.database,
            "region": self.region,
            "s3_staging_dir": self.s3_staging_dir,
            "role_arn": self.role_arn,
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
        base_url = f"snowflake://{self.user}:{self.password.get_decrypted_value()}@{self.account}/{self.database}"
        params = {
            "warehouse": self.warehouse,
            "role": self.role,
            "application": "swiple",
        }

        if schema:
            base_url += f"/{schema}"

        query_string = "&".join([f"{k}={v}" for k, v in params.items() if v])
        return f"{base_url}?{query_string}"

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
        placeholder='{"type": "service_account", "project_id": "...", "private_key_id": "...", "private_key": "...", "client_email": "...", "client_id": "...", "auth_uri": "...", "token_uri": "...", "auth_provider_x509_cert_url": "...", "client_x509_cert_url": "..."}',
    )

    def connection_string(self, dataset=None):
        connection = f"bigquery://{self.database}"
        if dataset is not None:
            connection = f"{connection}/{dataset}"
        if self.credentials_info:
            bas64_encoded_str_creds = base64.b64encode(
                self.credentials_info.get_decrypted_value().encode()
            ).decode()
            connection = f"{connection}?credentials_base64={bas64_encoded_str_creds}"
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
