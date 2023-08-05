from os import path
from unittest.mock import patch

import pytest
import rapidjson


@pytest.fixture
def gql_client_mock():
    retrieve_patch_obj = patch('algernon.aws.sapper.vinny.GqlClient.retrieve_flow_history')
    retrieve_patch_obj = patch('algernon.aws.sapper.vinny.GqlClient.retrieve_flow_history')
    mock_obj = retrieve_patch_obj.start()
    yield mock_obj
    retrieve_patch_obj.stop()


@pytest.fixture
def called_event():
    event = _read_test_event('called_event')
    return _generate_queued_event(event)


@pytest.fixture
def open_event_history():
    history = [_read_test_event('start_event')]
    return history


@pytest.fixture(autouse=True)
def silence_x_ray():
    x_ray_patch_all = 'algernon.aws.lambda_logging.patch_all'
    patch(x_ray_patch_all).start()
    yield
    patch.stopall()


@pytest.fixture
def mock_context():
    from unittest.mock import MagicMock
    context = MagicMock(name='context')
    context.__reduce__ = cheap_mock
    context.function_name = 'test_function'
    context.invoked_function_arn = 'test_function_arn'
    context.aws_request_id = '12344_request_id'
    context.get_remaining_time_in_millis.side_effect = [1000001, 500001, 250000, 0]
    return context


def cheap_mock(*args):
    from unittest.mock import Mock
    return Mock, ()


def _read_test_event(event_name):
    with open(path.join('tests', 'test_events', f'{event_name}.json')) as json_file:
        event = rapidjson.load(json_file)
        return event


def _generate_queued_event(event):
    event_string = rapidjson.dumps(event)
    message_object = {'Message': event_string}
    body_object = {'body': rapidjson.dumps(message_object)}
    return {'Records': [body_object]}
