import pytest
import unittest
from requests import get, post, put, delete


class TestApi:
    def test_get_all(self):
        assert get('http://127.0.0.1:8080/api/v2/jobs').json() == {'jobs': [{'team_leader': 1, 'job': 'Nothing',
                                                                               'id': 1, 'collaborators': '1, 2, 3', 'is_finished': False},
                                                                            {'team_leader': 1, 'job': 'Swimming',
                                                                             'id': 2, 'collaborators': '2, 3',
                                                                             'is_finished': False}
                                                                              ]}

    def test_post(self):
        assert post('http://127.0.0.1:8080/api/v2/jobs/3', json={'team_leader': 2, 'job': 'Nothing 2',
                                                                               'id': 3, 'collaborators': '1', 'is_finished': False}).json() == {
                   'success': 'OK'}

    def test_empty(self):  # пустой запрос возвращает именно Not found
        assert post('http://127.0.0.1:8080/api/v2/jobs', json={}).json() == {'error': 'Empty request'}

    def test_incorrect_post(self):
        assert post('http://127.0.0.1:8080/api/v2/jobs/3', json={'team_leader': 1, 'job': 'Nothing',
                                                                               'id': 2}).json() == {
                   'error': 'Bad request'}

    def test_correct_get_one(self):
        assert get('http://127.0.0.1:8080/api/v2/jobs/2').json() == {'team_leader': 1, 'job': 'Nothing',
                                                                               'id': 2, 'collaborators': '1, 2, 3', 'is_finished': False}

    def test_incorrect_get_one(self):
        assert get('http://127.0.0.1:8080/api/v2/jobs/10').json() == {'error': 'Not found'}

    def test_delete_correct(self):
        assert delete('http://127.0.0.1:8080/api/v2/jobs/1').json() == {'success': 'OK'}

    def test_delete_incorrect(self):
        assert delete('http://127.0.0.1:8080/api/v2/jobs/qwerty').json() == {'error': 'Not found'}
