import pytest

from app import create_app


@pytest.fixture(autouse=True)
def client():
    app = create_app()
    with app.test_client() as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
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


#
# @pytest.fixture(scope="session")
# def db(app, request):
#     """Session-wide test database."""
#     docker teardown could go here
#
# def teardown():
#     pass
#     broken models:
#     _db.drop_all()
#
# _db.app = app
# _db.create_all()
#
# request.addfinalizer(teardown)
# return _db
#
#
# @pytest.fixture(scope="function")
# def session(db, request):
#     """Creates a new database session for a test."""
#     connection = db.engine.connect()
#     transaction = connection.begin()
#
#     options = dict(bind=connection, binds={})
#     session = db.create_scoped_session(options=options)
#
#     db.session = session
#
#     def teardown():
#         transaction.rollback()
#         connection.close()
#         session.remove()
#
#     request.addfinalizer(teardown)
#     return session
#
#
# @pytest.fixture(scope="function")
# def base_user(session):
#     """Persists some basic models for common testing purposes."""
#     base_seeder()
#     user = User.query.filter_by(email="testsuperadmin@steplab.co").one()
#     g_realm_set(user.realm, user)
#     yield user
#
