
import pytest
import requests

from faker import Faker


names_auth = {}
names = []

urls_get = [
     'http://127.0.0.1:8000/api/v1/user/get?id=57576795',
     'http://127.0.0.1:8000/api/v1/user/get?username=ghorton'
]
token = ''


@pytest.mark.anyio
async def test_login():
     # 200 Response
     global token
     
     url = 'http://127.0.0.1:8000/api/v1/user/login' 
     
     data = {
          'username': 'vlados',
          'password': '1'
     }
     response = requests.post(url, data=data)
     assert response.status_code == 200
     token = response.json()['access_token']
     

@pytest.mark.anyio
async def test_login_invalid_password():
     # 403 Response
     
     url = 'http://127.0.0.1:8000/api/v1/user/login' 
     
     data = {
          'username': 'vlados',
          'password': '123'
     }
     response = requests.post(url, data=data)
     assert response.status_code == 403
     

@pytest.mark.anyio
async def test_login_user_not_exist():
     # 403 Response
     
     url = 'http://127.0.0.1:8000/api/v1/user/login'
     
     data = {
          'username': 'lexa',
          'password': '1'
     }
     response = requests.post(url, data=data)
     assert response.status_code == 403
     
     

@pytest.mark.anyio
async def test_signup():
     #  200 Response
     global names, names_auth
     
     fake = Faker()
     user = fake.user_name()

     url = 'http://127.0.0.1:8000/api/v1/user/signup'
     data = {
          'username': user,
          'password': '1'
     }
     response = requests.post(url, data=data)
     assert response.status_code == 200
     
     names.append(user)
     names_auth[user] = response.json()['access_token']
     
     
@pytest.mark.anyio
async def test_signup_user_exist():
     #  409 Response
     
     url = 'http://127.0.0.1:8000/api/v1/user/signup'
     
     data = {
          'username': 'vlados',
          'password': '17'
     }
     response = requests.post(url, data=data)
     assert response.status_code == 409
     
     
@pytest.mark.anyio
async def test_delete():
     # 200 Response
     global names, names_auth
     
     url = 'http://127.0.0.1:8000/api/v1/user/delete'
     
     auth = {'Authorization': f'Bearer {names_auth[names[0]]}'}
     
     response = requests.delete(url, headers=auth)
     assert response.status_code == 200
     del names[0]
     
     
@pytest.mark.anyio
async def test_delete_token_not_valid():
     # 401 Response
     
     url = 'http://127.0.0.1:8000/api/v1/user/delete'
     auth = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjk1MDA2Mzk3LCJpYXQiOjE3MjcxMDE5MzIsImV4cCI6MTcyNzEwMzczMiwicGVybSI6ZmFsc2V9.3-9Mbsq_Zzoy1uWtUzZop7zsU2Hqv6u1psjzc-0KpBs'}
     
     response = requests.delete(url, headers=auth)
     assert response.status_code == 401
     
     
@pytest.mark.anyio
async def test_get():
     # 200 Response
     global urls_get, token
     
     auth = {'Authorization': f'Bearer {token}'}

     response = requests.get(urls_get[0], headers=auth)
     assert response.status_code == 200
     del urls_get[0]
     
     
@pytest.mark.anyio
async def test_get_token_not_valid():
     # 401 Response
     
     url = 'http://127.0.0.1:8000/api/v1/user/get?username=ghorton'
     auth = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjk1MDA2Mzk3LCJpYXQiOjE3MjcxMDE5MzIsImV4cCI6MTcyNzEwMzczMiwicGVybSI6ZmFsc2V9.3-9Mbsq_Zzoy1uWtUzZop7zsU2Hqv6u1psjzc-0KpBs'}
     
     response = requests.get(url, headers=auth)
     assert response.status_code == 401
     
     
@pytest.mark.anyio
async def test_get_user_not_found():
     # 404 Response
     global token
     
     url = 'http://127.0.0.1:8000/api/v1/user/get?username=bulka'
     auth = {'Authorization': f'Bearer {token}'}
     
     response = requests.get(url, headers=auth)   
     assert response.status_code == 404  
     
     

     

     


