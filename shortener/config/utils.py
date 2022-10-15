from os import environ

from shortener.config.default import DefaultSettings


def get_settings() -> DefaultSettings:
    env = environ.get("ENV", "local1")
    # if env == "local":
    #     print(1)
    #     return DefaultSettings()
    return DefaultSettings()
