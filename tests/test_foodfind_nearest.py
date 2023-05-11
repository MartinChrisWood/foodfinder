from src.backend.frontend_handler import foodfind_nearest


def test_nearest():
    result = foodfind_nearest("postcode")
    print(result.head())
    assert result is not None
