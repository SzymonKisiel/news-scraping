import logging


class CommandHandlerService:
    logger: logging.Logger

    def __init__(self, logger: logging.Logger):
        self.logger = logger

