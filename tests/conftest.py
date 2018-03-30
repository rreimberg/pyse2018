
import pytest

from sample.app import create_app


@pytest.fixture(scope='session', autouse=True)
def app(request):
    """Session-wide test `Flask` application."""
    app = create_app()

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app
