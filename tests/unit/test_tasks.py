

from sample.models import User
from sample.tasks import save_on_database


def test_call_task_save_on_database(mocker):

    session_add_mock = mocker.patch('sample.tasks.db.session.add')
    session_commit_mock = mocker.patch('sample.tasks.db.session.commit')

    expected_user = User(
        uuid='uuid',
        name='username',
        email='fakeemail',
    )

    save_on_database('uuid', 'username', 'fakeemail')

    assert session_add_mock.call_count == 1
    assert session_add_mock.call_args == ((expected_user, ), )

    assert session_commit_mock.call_count == 1
