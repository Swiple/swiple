class SwipleError(Exception):
    pass


class SecretsError(SwipleError):
    pass


class SecretsModuleNotFoundError(SecretsError):
    pass


class SecretsKeyError(SecretsError):
    pass


class SecretClientError(SecretsError):
    pass
