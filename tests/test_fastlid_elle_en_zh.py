"""Test Elle ['en', 'zh']."""
from fastlid import fastlid


def test_elle_en_zh():
    """
    Test Elle ['en', 'zh'].

    TODO: fix short texts.
    """
    fastlid.set_languages = ["en", "zh"]
    try:
        res = fastlid("Elle")
    except Exception:
        res = ""
    assert res == ("en", 0.0)
