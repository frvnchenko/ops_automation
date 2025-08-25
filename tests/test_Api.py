
import pytest

from src.api.Api import Api


@pytest.mark.order(1)
def test_get_manual_index_ops():
    api_cl = Api()
    response = api_cl.get_manual_index_ops()
    assert response.status_code == 200, f"Ожидаемый код 200, но получен {response.status_code}"