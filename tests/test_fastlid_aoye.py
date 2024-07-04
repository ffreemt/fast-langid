from fastlid import fastlid

def test_fastlid_aoye():
    """Test fastlid 熬夜."""
    fastlid.set_languages = ["en", "zh"]
    assert fastlid("熬夜") ==  ('zh', 0.361)
