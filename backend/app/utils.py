from typing import Dict, Any

from app.settings import settings
import datetime
import emails
from emails.template import JinjaTemplate
from pathlib import Path
import json
import pytz
from copy import copy


def current_time():
    return str(datetime.datetime.utcnow().replace(tzinfo=pytz.utc))


def remove_t_from_date_string(date_string) -> datetime:
    """
    Converts a date string in the format
    2021-10-11T09:10:44.330614+00:00
    to
    2021-10-11 09:10:44.330614+00:00
    """
    return date_string.replace("T", " ")


def string_to_utc_time(date_string):
    """
    Converts a date string in the format
    2021-10-11 09:10:44.330614+00:00
    to
    2021-10-11T09:10:44.330614Z
    """
    return datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S.%f%z").strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def days_between_dates(start_date: datetime, end_date: datetime):
    return (end_date - start_date).days


def add_limit_clause(sql_query):
    query = copy(sql_query)
    query = query.replace(";", "").strip()
    if "limit" in query.lower():
        limit_value = query.rsplit(" ", 1)[-1]
        if limit_value.isdigit():
            query = query.lower().replace(f"limit {limit_value}", "limit 10")
    else:
        query = query + " limit 10"
    return query


def json_schema_to_single_doc(schema):
    max_tries = 100

    for i in range(max_tries):
        if '$ref' not in json.dumps(schema):
            break
        schema = replace_value_in_dict(schema.copy(), schema.copy())

    if schema.get("definitions"):
        del schema['definitions']

    return schema


def replace_value_in_dict(item, original_schema):
    if isinstance(item, list):
        return [replace_value_in_dict(i, original_schema) for i in item]
    elif isinstance(item, dict):
        if list(item.keys()) == ['$ref']:
            definitions = item['$ref'][2:].split('/')
            res = original_schema.copy()
            for definition in definitions:
                res = res[definition]
            return res
        else:
            return {key: replace_value_in_dict(i, original_schema) for key, i in item.items()}
    else:
        return item


def list_to_string_mapper(d, sep="."):
    def recurse(t, parent_key=""):
        if isinstance(t, list):
            for i in range(len(t)):
                recurse(t[i], parent_key + sep + str(i) if parent_key else str(i))
        if isinstance(t, dict):
            for k, v in t.items():
                if isinstance(v, list):
                    t[k] = json.dumps(v)
                else:
                    recurse(v, parent_key + sep + k if parent_key else k)
        elif isinstance(t, (str, bool, int, float, type(None))):
            pass
        else:
            raise NotImplementedError(f't is of type, {type(t)}, which is not implemented.')
    recurse(d)
    return d


def error_msg_from_exception(ex: Exception) -> str:
    """Translate exception into error message
    Database have different ways to handle exception. This function attempts
    to make sense of the exception object and construct a human readable
    sentence.
    """
    msg = ""
    if hasattr(ex, "message"):
        if isinstance(ex.message, dict):
            msg = ex.message.get("message")
        elif ex.message:
            msg = ex.message
    return msg or str(ex)
# def send_email(
#     email_to: str,
#     subject_template: str = "",
#     html_template: str = "",
#     environment: Dict[str, Any] = {},
# ) -> None:
#     assert settings.EMAILS_ENABLED, "no provided configuration for email variables"
#     message = emails.Message(
#         subject=JinjaTemplate(subject_template),
#         html=JinjaTemplate(html_template),
#         mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
#     )
#     smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
#     if settings.SMTP_TLS:
#         smtp_options["tls"] = True
#     if settings.SMTP_USER:
#         smtp_options["user"] = settings.SMTP_USER
#     if settings.SMTP_PASSWORD:
#         smtp_options["password"] = settings.SMTP_PASSWORD
#     response = message.send(to=email_to, render=environment, smtp=smtp_options)
#     print(f"Send email result: {str(response)}.")
#
#
# def send_test_email(email_to: str) -> None:
#     project_name = settings.PROJECT_NAME
#     subject = f"{project_name} - Test email"
#     with open(Path(settings.EMAIL_TEMPLATES_DIR) / "test_email.html") as f:
#         template_str = f.read()
#     send_email(
#         email_to=email_to,
#         subject_template=subject,
#         html_template=template_str,
#         environment={"project_name": settings.PROJECT_NAME, "email": email_to},
#     )
#
#
# def send_reset_password_email(email_to: str, email: str, token: str) -> None:
#     project_name = settings.PROJECT_NAME
#     subject = f"{project_name} - Password recovery for user {email}"
#     with open(Path(settings.EMAIL_TEMPLATES_DIR) / "reset_password.html") as f:
#         template_str = f.read()
#     server_host = settings.SERVER_HOST
#     link = f"{server_host}/reset-password?token={token}"
#     send_email(
#         email_to=email_to,
#         subject_template=subject,
#         html_template=template_str,
#         environment={
#             "project_name": settings.PROJECT_NAME,
#             "username": email,
#             "email": email_to,
#             "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
#             "link": link,
#         },
#     )
#
#
# def send_new_account_email(email_to: str, username: str, password: str) -> None:
#     project_name = settings.PROJECT_NAME
#     subject = f"{project_name} - New account for user {username}"
#     with open(Path(settings.EMAIL_TEMPLATES_DIR) / "new_account.html") as f:
#         template_str = f.read()
#     link = settings.SERVER_HOST
#     send_email(
#         email_to=email_to,
#         subject_template=subject,
#         html_template=template_str,
#         environment={
#             "project_name": settings.PROJECT_NAME,
#             "username": username,
#             "password": password,
#             "email": email_to,
#             "link": link,
#         },
#     )


# def generate_password_reset_token(email: str) -> str:
#     delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
#     now = datetime.datetime.utcnow()
#     expires = now + delta
#     exp = expires.timestamp()
#     encoded_jwt = jwt.encode(
#         {"exp": exp, "nbf": now, "sub": email}, settings.SECRET_KEY, algorithm="HS256",
#     )
#     return encoded_jwt

#
# def verify_password_reset_token(token: str) -> Optional[str]:
#     try:
#         decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
#         return decoded_token["email"]
#     except jwt.JWTError:
#         return None
