"""Run main()."""

from fastlid import fastlid
import logzero
from logzero import logger

logzero.setup_logger(level=20)


def main(text, k=1):
    """Run main()"""
    if k == 22:
        logger.info("Testing set_languages = ['en', 'de']")
        k = 2

        fastlid.set_languages = ["en", "de"]

    logger.debug(fastlid(text, k=k))


if __name__ == "__main__":
    import sys

    logger.debug(sys.argv)

    try:
        k = int(sys.argv[1])
    except Exception as e:
        logger.error(e)
        k = 1

    try:
        text = str(sys.argv[2])
    except Exception as e:
        logger.error(e)
        text = "test"

    logger.info("text: %s", text)
    main(text, k)
