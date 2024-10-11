
import pytest
import requests



api_token = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjc1ODY5MDMyMTEwMjg0Njc2LCJpYXQiOjE3MjgwNjM4MDEsImV4cCI6MTcyODA2NTYwMSwicGVybSI6ZmFsc2V9.HESlmpGyisZ7_fC8mhqNuo7NySOelSvHk4yxvPlXb30'
main_url = 'http://127.0.0.1:8000/api/v1/forum/question'
auth = {'Authorization': api_token}


@pytest.mark.anyio
def test_create_question():
     # Response 200
     global auth, main_url
     
     json = {'question': 'Где моя сосиска?'}
     url = main_url + '/create?category=sport'
     
     response = requests.post(
          url=url,
          json=json,
          headers=auth
     )
     assert response.status_code == 200
     
     
@pytest.mark.anyio
def test_get_question():
     # Response 200
     global auth, main_url
     
     url = main_url + '/get/' + '35396495'
     
     response = requests.get(
          url=url,
          headers=auth
     )
     assert response.status_code == 200
     
     
@pytest.mark.anyio
def test_get_user_questions():
     # Response 200
     global auth, main_url
     
     username, id = 'vlados', '57576795'
     
     url_id = main_url + f'/user_questions?id={id}'
     url_name = main_url + f'/user_questions?username={username}'
     
     response_id = requests.get(
          url=url_id,
          headers=auth
     )
     response_username = requests.get(
          url=url_name,
          headers=auth
     )
     assert response_id.status_code == 200 and response_username.status_code == 200
     
     
@pytest.mark.anyio
def test_update_question():
     # Response 200
     global auth, main_url
     
     url = main_url + '/update/' + '35396495'
     question = {'new_question': 'Кто сожрал сосиську?'}
     
     response = requests.patch(
          url=url,
          json=question,
          headers=auth
     )
     assert response.status_code == 200
     
     
@pytest.mark.anyio
def test_delete_question():
     # Response 200
     global auth, main_url
     
     url = main_url + '/delete/' + '25717917'
     
     response = requests.delete(
          url=url,
          headers=auth
     )
     assert response.status_code == 200
     
     
