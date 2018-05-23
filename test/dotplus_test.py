import json

import pytest
import requests

import dotplus
import mock


@mock.patch('requests.post')
def test_login_should_return_credentials(mock_post):
    mock_post.return_value = _create_successful_login_response()

    config = create_config_for_tests()
    credentials = dotplus.login(config)

    assert credentials.client_id is not None
    assert credentials.token is not None
    assert credentials.config == config


@mock.patch('requests.post')
def test_login_with_invalid_credentials_should_raise(mock_post):
    mock_post.return_value = _create_invalid_credentials_login_response()

    config = create_config_with_invalid_credentials()
    with pytest.raises(dotplus.InvalidCredentialsError):
        dotplus.login(config)


@mock.patch('requests.post')
def test_login_with_connection_timeout_should_raise(mock_post):
    mock_post.return_value = _create_timeout_login_response()

    config = create_config_for_timeout()
    with pytest.raises(Exception):
        dotplus.login(config)


@mock.patch('requests.get')
def test_time_cards_should_return_time_cards(mock_get):
    mock_get.return_value = _create_successful_time_cards_response()
    credentials = create_credentials_for_tests()

    time_cards = dotplus.time_cards(credentials)

    first_time_card = time_cards[0]

    assert len(time_cards) > 0
    assert isinstance(time_cards, list)

    assert first_time_card['date']
    assert isinstance(first_time_card['time_cards'], list)


def create_credentials_for_tests():
    return dotplus.Credentials(
        'some-token',
        'some-client_id',
        create_config_for_tests(),
    )


def create_config_for_tests():
    return dotplus.config.Config(
        'some_email@mailprovider.com',
        'some_very_secret_password',
        'https://api.somefakehost.com/signin',
        'https://api.somefakehost.com/timecards'
    )


def create_config_with_invalid_credentials():
    return dotplus.config.Config(
        'invalid_email@email.com',
        'invalid_password',
        'https://api.somefakehost.com/signin',
        'https://api.somefakehost.com/timecards'
    )


def create_config_for_timeout():
    return dotplus.config.Config(
        'any_email@email.com',
        'any_password',
        'https://api.somefakehost.com/signin',
        'https://api.somefakehost.com/timecards'
    )


def _create_successful_login_response():
    mock_resp = mock.Mock()
    mock_resp.status_code = 201
    mock_resp.json = lambda: _get_json('successful_login.json')
    return mock_resp


def _create_invalid_credentials_login_response():
    mock_resp = mock.Mock()
    mock_resp.status_code = 401
    mock_resp.json = lambda: _get_json('invalid_credentials_login.json')
    return mock_resp


def _create_timeout_login_response():
    mock_resp = mock.Mock()
    mock_resp.raise_for_status = mock.Mock()
    mock_resp.raise_for_status.side_effect = requests.exceptions.ConnectionError()
    return mock_resp


def _create_successful_time_cards_response():
    mock_resp = mock.Mock()
    mock_resp.status_code = 201
    mock_resp.json = lambda: _get_json('successful_time_cards.json')
    return mock_resp


def _get_json(filename):
    with open(f'test/sample_responses/{filename}') as json_data:
        return json.load(json_data)
