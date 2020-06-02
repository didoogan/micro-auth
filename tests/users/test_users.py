import unittest

import pytest
import nest_asyncio


nest_asyncio.apply()



@pytest.mark.asyncio
class TestUsers:

    async def test_signup_success(self, client, user_data, user_manager):
        response = client.post('users/signup', json=user_data)
        assert response.status_code == 201
        db_user = await user_manager.get_by_email(user_data['email'])
        assert db_user.email == user_data['email']

    def test_signup_duplicate_user(self, client, user_data):
        client.post('users/signup', json=user_data)
        response = client.post('users/signup', json=user_data)
        assert response.status_code == 400

    @pytest.mark.parametrize('email, password', (
        ['not_email', 'password123'],
        ['test@test.com', 'looooooooooooooooooooooooooooooooooooong password'],
        ['teset@test.com', '123'],
    ))
    def test_signup_wrong_payload(self, client, email, password):
        payload = {'email': email, 'password': password}
        print(payload)
        response = client.post('users/signup', json=payload)
        assert response.status_code == 422

    def test_signin_success(self, client, user_data):
        client.post('users/signup', json=user_data)
        response = client.post('users/signin', json=user_data)
        assert response.status_code == 200

    def test_signin_fail(self, client):
        wrong_payload = {'email': 'wrong@wrong.com', 'password': 'password123'}
        response = client.post('users/signin', json=wrong_payload)
        assert response.status_code == 400

    def test_user_info_success(self, client, user_data):
        response = client.post('users/signup', json=user_data)
        token = response.json()['token']
        response = client.get(
            'users/user-info',
            headers={'Authentication': token},
        )
        assert response.status_code == 200
        assert response.json()['email'] == user_data['email']

    @pytest.mark.parametrize('wrong_token', ['', 'dich' * 10])
    def test_user_info_fail(self, client, wrong_token):
        response = client.get(
            'users/user-info',
            headers={'Authentication': wrong_token},
        )
        assert response.status_code == 422
