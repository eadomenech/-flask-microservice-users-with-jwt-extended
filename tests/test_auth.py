import json

from flask import current_app

from tests.utils import TestBaseModel


class TestAuth(TestBaseModel):
    """Tests for the Auth."""

    def test_registered_user_login(self, client):
        self.add_user()
        response = client.post(
            '/api/v1/auth/login',
            data=json.dumps({
                'email': 'user1@example.com',
                'password': 'p@ssw0rd'}),
            content_type='application/json',
        )
        data = json.loads(response.data.decode())
        assert data['status'] == "success"
        assert data['msg'] == "Successfully logged in."
        assert data['token']
        assert response.content_type == 'application/json'
        assert response.status_code == 200

    def test_not_registered_user_login(self, client):
        response = client.post(
            '/api/v1/auth/login',
            data=json.dumps({
                'email': 'user1@example.com',
                'password': 'p@ssw0rd'}),
            content_type='application/json',
        )
        data = json.loads(response.data.decode())
        assert data['status'] == "fail"
        assert data['msg'] == "User does not exist."
        assert data['token'] == ''
        assert response.content_type == 'application/json'
        assert response.status_code == 404

    def test_registered_user_login_wrong_password(self, client):
        self.add_user()
        response = client.post(
            '/api/v1/auth/login',
            data=json.dumps({
                'email': 'user1@example.com',
                'password': 'otherp@ssw0rd'}),
            content_type='application/json',
        )
        data = json.loads(response.data.decode())
        assert data['status'] == "fail"
        assert data['msg'] == "Incorrect password."
        assert data['token'] == ''
        assert response.content_type == 'application/json'
        assert response.status_code == 404

    def test_valid_logout(self, client):
        self.add_user()
        resp_login = client.post(
            '/api/v1/auth/login',
            data=json.dumps({
                'email': 'user1@example.com', 'password': 'p@ssw0rd'
            }),
            content_type='application/json'
        )
        # valid token logout
        token = json.loads(resp_login.data.decode())['token']
        response = client.get(
            '/api/v1/auth/logout',
            headers={'Authorization': f'Bearer {token}'}
        )
        data = json.loads(response.data.decode())
        assert data['status'] == 'success'
        assert data['msg'] == 'Successfully logged out.'
        assert response.status_code == 200

    def test_invalid_logout_expired_token(self, client):
        self.add_user()
        current_app.config['JWT_ACCESS_TOKEN_EXPIRES'] = -1
        resp_login = client.post(
            '/api/v1/auth/login',
            data=json.dumps({
                'email': 'user1@example.com',
                'password': 'p@ssw0rd'}),
            content_type='application/json'
        )
        token = json.loads(resp_login.data.decode())['token']
        response = client.get(
            '/api/v1/auth/logout',
            headers={'Authorization': f'Bearer {token}'}
        )
        data = json.loads(response.data.decode())
        assert data['status'] == 'fail'
        assert data['msg'] == 'The access token has expired. Please log ' +\
            'in again.'
        assert response.status_code == 401

    def test_invalid_logout(self, client):
        response = client.get(
            '/api/v1/auth/logout',
            headers={'Authorization': 'Bearer invalid'})
        data = json.loads(response.data.decode())
        assert data['status'] == 'fail'
        assert data['msg'] == 'Invalid token. Please log in again.'
        assert response.status_code == 401

    def test_user_status(self, client):
        self.add_user()
        resp_login = client.post(
            '/api/v1/auth/login',
            data=json.dumps({
                'email': 'user1@example.com',
                'password': 'p@ssw0rd'
            }),
            content_type='application/json'
        )
        token = json.loads(resp_login.data.decode())['token']
        response = client.get(
            '/api/v1/auth/status',
            headers={'Authorization': f'Bearer {token}'}
        )
        data = json.loads(response.data.decode())
        assert data['status'] == 'success'
        assert data['data']
        assert data['data']['username'] == 'user1'
        assert data['data']['active']
        assert response.status_code == 200

    def test_invalid_status(self, client):
        response = client.get(
            '/api/v1/auth/status',
            headers={'Authorization': 'Bearer invalid'})
        data = json.loads(response.data.decode())
        assert data['status'] == 'fail'
        assert data['msg'] == 'Invalid token. Please log in again.'
        assert response.status_code == 401

    def test_register_user(self, client):
        """Ensure a new test_add_user can be added to the database."""
        response = client.post(
            '/api/v1/auth/register',
            data=json.dumps({
                'username': 'user1', 'email': 'user1@example.com',
                'password': 'p@ssw0rd'}),
            content_type='application/json',
        )
        data = json.loads(response.data)
        assert response.status_code == 201
        assert response.content_type == 'application/json'
        assert data['status'] == "success"
        assert data['msg'] == "Successfully registered."

    def test_add_user_invalid_json(self, client):
        """Ensure error is thrown if the JSON object is empty."""
        response = client.post(
            '/api/v1/auth/register',
            data=json.dumps({}),
            content_type='application/json',
        )
        data = json.loads(response.data)
        assert response.status_code == 400
        message = 'Missing data for required field.'
        assert message in data['messages']['json']['username']
        assert message in data['messages']['json']['email']

    def test_add_user_invalid_json_keys_username(self, client):
        """
        Ensure error is thrown if the JSON object does not have a username key.
        """
        response = client.post(
            '/api/v1/auth/register',
            data=json.dumps({
                'email': 'user1@example.com', 'password': 'p@ssw0rd'
            }),
            content_type='application/json',
        )
        data = json.loads(response.data)
        assert response.status_code == 400
        message = 'Missing data for required field.'
        assert message in data['messages']['json']['username']

    def test_add_user_invalid_json_keys_email(self, client):
        """
        Ensure error is thrown if the JSON object does not have a email
        key.
        """
        response = client.post(
            '/api/v1/auth/register',
            data=json.dumps({
                'username': 'user1', 'password': 'p@ssw0rd'
            }),
            content_type='application/json',
        )
        data = json.loads(response.data)
        assert response.status_code == 400
        message = 'Missing data for required field.'
        assert message in data['messages']['json']['email']

    def test_add_user_invalid_json_keys_password(self, client):
        """
        Ensure error is thrown if the JSON object does not have a password
        key.
        """
        response = client.post(
            '/api/v1/auth/register',
            data=json.dumps({
                'username': 'user1', 'email': 'user1@example.com'
            }),
            content_type='application/json',
        )
        data = json.loads(response.data)
        assert response.status_code == 400
        message = 'Missing data for required field.'
        assert message in data['messages']['json']['password']

    def test_add_user_duplicate_username(self, client):
        """Ensure error is thrown if the username already exists."""
        client.post(
            '/api/v1/auth/register',
            data=json.dumps({
                'username': 'user1', 'email': 'user1@example.com',
                'password': 'p@ssw0rd'
            }),
            content_type='application/json',
        )
        response = client.post(
            '/api/v1/auth/register',
            data=json.dumps({
                'username': 'user1', 'email': 'user2@example.com',
                'password': 'p@ssw0rd2'
            }),
            content_type='application/json',
        )
        data = json.loads(response.data)
        assert response.status_code == 400
        message = 'Sorry. That user already exists.'
        assert message in data['msg']
        assert 'fail' in data['status']

    def test_add_user_duplicate_email(self, client):
        """Ensure error is thrown if the email already exists."""
        client.post(
            '/api/v1/auth/register',
            data=json.dumps({
                'username': 'user1', 'email': 'user1@example.com',
                'password': 'p@ssw0rd'
            }),
            content_type='application/json',
        )
        response = client.post(
            '/api/v1/auth/register',
            data=json.dumps({
                'username': 'user2', 'email': 'user1@example.com',
                'password': 'p@ssw0rd2'
            }),
            content_type='application/json',
        )
        data = json.loads(response.data)
        assert response.status_code == 400
        message = 'Sorry. That user already exists.'
        assert message in data['msg']
        assert 'fail' in data['status']
