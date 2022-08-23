"""Detect lang via a fasttext model.

"""
from typing import Any, Callable, List, Optional, Tuple, Union

from pathlib import Path
import re
import urllib.request
import hashlib
import numpy as np
import fasttext
import logzero
from logzero import logger

from fastlid import supported_langs

# patch warning from fasttext
fasttext.FastText.eprint = lambda x: None

# logzero.setup_default_logger(level=20)

# logger.info(__file__)
_ = Path(__file__).parent
MODEL_FILE = "lid.176.bin"
MODEL_FILE = "lid.176.ftz"

# https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin

MODEL_PATH = Path(_) / MODEL_FILE

# check MODEL_PATH exist and md5 is correct
if not MODEL_PATH.exists():
    logger.debug("fetching %s (once only)", MODEL_FILE)
    URL = "https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.ftz"

    # _ = Path(URL).name
    try:
        response = urllib.request.urlopen(URL)
    except Exception as e:
        logger.error(e)
        raise SystemExit(1) from e
    try:
        logger.info("Downloading %s (need to do this just once)", URL)
        data = response.read()
        Path(MODEL_PATH).write_bytes(data)
    except Exception as e:
        logger.error(e)
        raise SystemExit(1) from e

MD5 = hashlib.md5(MODEL_PATH.read_bytes()).hexdigest()
EXPECTED = "340156704bb8c8e50c4abf35a7ec2569"
assert MD5 == EXPECTED, f"md5 mismtach (md5 != expected): {MD5} != {EXPECTED}"

try:
    MODEL = fasttext.load_model(str(MODEL_PATH))
except Exception as e:
    logger.error(e)
    raise SystemExit(1) from e


def with_func_attrs(**attrs: Any) -> Callable:
    """Define func_attrs."""

    def with_attrs(fct: Callable) -> Callable:
        for key, val in attrs.items():
            setattr(fct, key, val)
        return fct

    return with_attrs


# fmt: off
@with_func_attrs(set_languages=None)
def fastlid(  # noqa: C901
        text: str,
        k: int = 1,
        threshold: float = 0.0,
        loglevel: int = 20,
        method: Optional[int] = None,
) -> Union[Tuple[str, float], Tuple[List[str], List[float]]]:
    # fmt: on
    r"""Detect lang via a fasttext model.

        Given a string, get a list of labels and a list of
    corresponding probabilities. k controls the number
    of returned labels. A choice of 5, will return the 5
    most probable labels. By default this returns only
    the most likely label and probability. threshold filters
    the returned labels by a threshold on probability. A
    choice of 0.5 will return labels with at least 0.5
    probability. k and threshold will be applied together to
    determine the returned labels.

    Args:
        text:
        k: top k
            when k=1 -> Tuple[str, float]
            when k > 1 -> Tuple[List[str], List[float]]

            langid.langid.classify('test')
            # ('de', 8.41027545928955)
            langid.langid.set_languages(['de','fr','it'])
            -> fastlid.set_languages = ['de','fr','it']

            if fastlid.set_languages is not None:
                model.predict(text, k=-1)
                retrieve according to fastlid.set_languages and k
                normalize prob.
            else:
                just model.predict(text)

            further process -> Tuple(str, float)
        threshold: filters the returned labels by a
                threshold on probability
                fasttext.load_model().predict(..., threshold=0.0)
        method: regarding how to insert spaces
                None: default, using re.sub(r"(?<=[a-zA-Z]) (?=[a-zA-Z])", "", text.replace("", " "))
                else: using re.sub(r"[一-龟]|\d+|\w+", r"\g<0> ", text)
    Returns:
        for k=1: (label, probabilty)
        for k>1: ([label1, ..., labelk], [prob1, ..., probk]
    """
    try:
        loglevel = int(loglevel)
    except Exception as e:
        logger.error(e)
        loglevel = 20
    if loglevel < 10:
        loglevel = 10
    logzero.setup_default_logger(level=loglevel)

    # logger.debug("fastlid entry")

    try:
        text = str(text)
    except Exception as e:
        logger.error("Cant convert to text: %s", e)
        raise SystemExit(1) from e
    try:
        # insert some spaces in Chinese text
        # text = re.sub(r"[一-龟]", r" \g<0> ", text)

        # ispace = lambda text: re.sub(r"(?<=[a-zA-Z\d]) (?=[a-zA-Z\d])", "", text.replace("", " ")).strip()

        if method is None:
            text = re.sub(r"(?<=[a-zA-Z]) (?=[a-zA-Z])", "", text.replace("", " "))  # NOQA
        else:
            # faster? method 3 in insert_spaces
            # text = re.sub(r"[一-龟]|\d+|\w+", r"\g<0> ", text)
            text = re.sub(r"[\u4e00-\u9fef]|\d+|\w+", r"\g<0> ", text)

        # probably better, need to check speed,
        # slow 30s to process shakespeare
        # text = re.sub(r"[一-龟]|[^一-龟]+", r"\g<0> ", text)

        # faster, but cant be used here
        # text = text.replace("", " ")
    except Exception as e:
        logger.error("re.sub error: %s, we proceed nevertheless", e)

    # \n seems to cause problems
    text = text.replace("\n", " ")

    # verify fastlid.set_languages is a list
    if fastlid.set_languages is not None:
        if not isinstance(fastlid.set_languages, list):
            logger.error("fastlid.set_languages is not a list")
            logger.info("Setting to None")
            fastlid.set_languages = None

        logger.debug("fastlid.set_languages: %s", fastlid.set_languages)

    if not fastlid.set_languages:  # None or empty
        try:
            res = MODEL.predict(text, k=k, threshold=threshold)
        except Exception as e:
            logger.error("MODEL.predict error: %s", e)
            raise

        try:
            lid, prob = list(res[0]), res[1].tolist()
        except Exception as e:
            logger.error(e)
            lid, prob = [], []

        if k > 1:
            return [*map(lambda x: x[9:], lid)], [*map(lambda x: round(x, 3), prob)]

        return [*map(lambda x: x[9:], lid)][0], [*map(lambda x: round(x, 3), prob)][0]

        # return ["en"], [1]

    # #### fastlid.set_languages is not None  ####
    # make sure set_languages is valid in supported_langs
    logger.debug("set_languages: %s", fastlid.set_languages)

    # strip spaces, conver to lower case
    try:
        fastlid.set_languages = [elm.strip().lower() for elm in fastlid.set_languages if elm.strip()]
    except Exception as e:
        logger.error("fastlid.set_languages ill-formed: %s", e)
        raise SystemExit(1) from e

    valid = True
    for elm in fastlid.set_languages:
        if elm not in supported_langs:
            logger.error("%s not in supported_langs", elm)

            # set flag and remove value
            valid = False
            fastlid.set_languages.remove(elm)
    if not valid:
        logger.warning(" one or more languages set in set_languages not in supported langs: %s", supported_langs)
        # raise SystemExit(1)
        logger.info("We'll just disgard those and proceed")

    # fetch all possible langs
    try:
        ires = MODEL.predict(text, -1, threshold=threshold)  # k=-1
    except Exception as e:
        logger.error("MODEL.predict error: %s", e)
        raise

    # logger.debug("ires, %s, %s", ires[0], ires[1])

    # filter out based on set_languages
    lid, prob = [], []
    for elm0, elm1 in zip(ires[0], ires[1]):
        if elm0[9:] in fastlid.set_languages:
            lid.append(elm0)
            prob.append(elm1)

    logger.debug("lid: %s", lid)
    logger.debug("prob: %s", prob)

    lid = np.array(lid)
    prob = np.array(prob)

    # qick fix, need to check later on
    if fastlid.set_languages is not None:
        len_l = len(fastlid.set_languages)
        if k > len_l:
            logger.warning("k (=%s) > len(fastlid.set_languages) (%s) makes no sense, k reset to %s", k, len_l, len_l)
            # k = 1
            k = len_l

    # no need, already sorted, just take the first k terms
    # ind = np.argpartition(prob, -1 * k)[-1 * k:]
    # prob = prob[ind]
    # lid = lid[ind]

    # lid are: '__label__en', '__label__de', hence 9:
    if k > 1:
        return [*map(lambda x: x[9:], lid[:k])], [*map(lambda x: round(x, 3), prob[:k])]

    try:
        _ = [*map(lambda x: x[9:], lid)][0], [*map(lambda x: round(x, 3), prob)][0]
    except Exception as exc:
        logger.debug(" lid: %s", lid)
        logger.error(exc)
        raise
    return _
