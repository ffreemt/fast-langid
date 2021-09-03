from fastlid import fastlid


def test_fastlid():
    """Test fastlid 'test'."""
    # assert fastlid("a") == ("en", 1)
    # assert fastlid("") == (['en'], [0.125])
    assert fastlid("test") == ("hu", 0.275)


def test_fastlidk2():
    """Test fastlid 'test'."""
    fastlid.set_languages = ["de", "zh"]

    # assert fastlid('test') == ('de', 0.275)
    assert fastlid("test") == ("zh", 0.01)


def test_de_en():
    """Test de_en."""
    fastlid.set_languages = ["en", "de"]

    text = "test it and more what how can this be 中"
    assert fastlid(text, k=2) == (["en", "de"], [0.405, 0.001])


def test_slashhelp():
    """Test /help."""
    text = "/help"
    assert fastlid(text)[0] in ("en",)
