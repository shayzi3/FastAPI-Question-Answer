
import pytest
import requests


@pytest.mark.anyio
async def test_root():
     url = 'http://127.0.0.1:8000/'
     
     response = requests.get(url)
     assert response.json() == {'message': 'Hello my friend!'}