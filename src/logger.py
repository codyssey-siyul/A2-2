import logging


def setup_logger(name: str = "news_pipeline"):
    logger = logging.getLogger(name)

    # 중복 핸들러 등록 방지
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger