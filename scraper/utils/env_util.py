import os


def is_docker() -> bool:
    return os.getenv('IS_DOCKER', default=False)
