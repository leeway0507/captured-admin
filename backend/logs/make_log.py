import logging
import os


def make_logger(path, name):
    if not os.path.exists(path):
        dir = path.rsplit("/", 1)[0]
        os.makedirs(dir, exist_ok=True)

    # 1 logger instance를 만든다.
    logger = logging.getLogger(name)
    logger.propagate = False

    # 2 logger의 level을 가장 낮은 수준인 DEBUG로 설정해둔다.
    logger.setLevel(logging.DEBUG)

    # 3 formatter 지정
    formatter = logging.Formatter(
        "%(levelname)s: %(asctime)s - %(name)s - %(funcName)s - %(message)s",
        datefmt="%Y/%m/%d %H:%M:%S",
    )

    # 4 handler instance 생성
    file_handler = logging.FileHandler(filename=path, mode="a")
    stream_handler = logging.StreamHandler()

    # 5 handler 별로 다른 level 설정
    file_handler.setLevel(logging.DEBUG)
    stream_handler.setLevel(logging.WARNING)

    # 6 handler 출력 format 지정
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    # 7 logger에 handler 추가
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger


def make_monitoring_logger(name=None):
    # 1 logger instance를 만든다.
    logger = logging.getLogger(name)

    # 2 logger의 level을 가장 낮은 수준인 DEBUG로 설정해둔다.
    logger.setLevel(logging.DEBUG)

    # 3 formatter 지정
    formatter = logging.Formatter(
        "%(levelname)s: %(asctime)s - %(name)s - %(funcName)s - %(message)s"
    )

    # 4 handler instance 생성
    stream_handler = logging.StreamHandler()

    # 5 handler 별로 다른 level 설정
    stream_handler.setLevel(logging.DEBUG)

    # 6 handler 출력 format 지정
    stream_handler.setFormatter(formatter)

    # 7 logger에 handler 추가
    logger.addHandler(stream_handler)

    return logger
