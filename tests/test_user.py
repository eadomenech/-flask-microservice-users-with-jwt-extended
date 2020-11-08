import json

from tests.utils import TestBaseModel


class TestUsersService(TestBaseModel):
    """Tests for the Users Service."""

    def test_single_user(self, client):
        """Ensure get single user behaves correctly."""
        user = self.add_user()
        response = client.get(f'/api/v1/user/{user.id}')
        data = json.loads(response.data.decode())

        assert response.status_code == 200
        assert 'success' in data['status']
        assert 'user1' in data['data']['username']
        assert 'user1@example.com' in data['data']['email']
        assert data['data']['active']

    def test_single_user_no_id(self, client):
        """Ensure error is thrown if an id is not provided."""
        response = client.get('/api/v1/user/blah')
        data = json.loads(response.data.decode())
        assert response.status_code == 404
        assert data['status'] == 'fail'
        assert 'User does not exist' in data['msg']

    def test_single_user_incorrect_id(self, client):
        """Ensure error is thrown if the id does not exist."""
        response = client.get('/api/v1/user/999')
        data = json.loads(response.data.decode())
        assert response.status_code == 404
        assert data['status'] == 'fail'
        assert 'User does not exist' in data['msg']

    def test_all_users(self, client):
        """Ensure get all users behaves correctly."""
        self.add_user()
        self.add_user(
            username='user2', email='user2@example.com',
            password='p@ssw0rd')
        response = client.get('api/v1/users')
        data = json.loads(response.data.decode())

        assert response.status_code == 200
        assert len(data['data']) == 2

        assert 'user1' in data['data'][0]['username']
        assert 'user1@example.com' in data['data'][0]['email']
        assert data['data'][0]['active'] == True

        assert 'user2' in data['data'][1]['username']
        assert 'user2@example.com' in data['data'][1]['email']
        assert data['data'][1]['active'] == True
