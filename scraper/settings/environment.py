import os


def is_docker():
    return os.environ.get('IS_DOCKER', False)
