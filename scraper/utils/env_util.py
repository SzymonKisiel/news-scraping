import os


def is_docker() -> bool:
    return os.getenv('IS_DOCKER', default=False)


def is_benchmark() -> bool:
    return os.getenv('IS_BENCHMARK', default=False)
