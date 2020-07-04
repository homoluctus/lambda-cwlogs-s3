import logging


def get_logger(name: str = __name__) -> logging.Logger:
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    # ltsv形式
    log_format = (
        "time:%(asctime)s\tseverity:%(levelname)s\t"
        + "module:%(module)s\tlineno:%(lineno)d\tmessage:%(message)s"
    )
    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    return logger
