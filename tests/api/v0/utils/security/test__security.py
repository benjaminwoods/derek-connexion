import pytest
from datetime import datetime
import os
from hashlib import sha3_512

from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

from api.v0.utils.security import _security
from api.v0.utils.security import _user

@pytest.fixture(scope="function")
def engine(monkeypatch):
    return create_engine("sqlite+pysqlite:///:memory:", echo=True)

@pytest.fixture(scope="function")
def metadata(engine):
    return MetaData()

@pytest.fixture(scope="function")
def users_table(metadata):
    return Table(
        'users',
        metadata,
        Column('_id', Integer, primary_key=True),
        Column('name', String(50), nullable=False, unique=True),
        Column('password', String(128), nullable=False),
        Column('salt', String(50), nullable=False),
        Column('createdAt', DateTime, nullable=False),
        Column('lastEdited', DateTime, nullable=False),
    )

@pytest.fixture(scope="function")
def session(engine):
    with Session(engine) as session:
        yield session

@pytest.fixture(scope="function")
def put_users_table(metadata, engine, users_table):
    try:
        metadata.drop_all(engine, [users_table])
    except:
        pass

    metadata.create_all(engine, [users_table])

@pytest.fixture(scope="function")
def mock_engine(engine, monkeypatch):
    monkeypatch.setattr(_security, "engine", engine)

class Test_basic_auth:
    def test_empty_table(self, put_users_table, mock_engine):
        """Given that I have a users table
        And that table is empty
        When I authenticate user "user1"
        Then None is returned
        """
        # When
        result = _security.basic_auth(username="user1", password="abcdef")

        # Then
        assert result is None
    def test_no_user(self, put_users_table, session, mock_engine):
        """Given that I have a users table
        And that table contains one user "user1"
        When I authenticate user "user2"
        Then None is returned
        """
        # Given
        _user._postOne(session, _user.User(
            name="user1",
            password="abcdef",
            salt="salt1",
            createdAt=datetime.now(),
            lastEdited=datetime.now(),
        )) 

        # When
        result = _security.basic_auth(username="user2", password="abcdef")

        # Then
        assert result is None
    def test_password_matches(self, put_users_table, session, mock_engine):
        """Given that I have a users table
        And that table contains one user "user1"
        When I authenticate user "user1"
        And I use the correct password
        Then the user identity is returned
        """
        # Given
        SALT = "salt1"
        PASSWORD = "abc123"
        HASHED_PASSWORD = sha3_512((SALT + PASSWORD).encode("utf-8")).hexdigest()
        _user._postOne(session, _user.User(
            name="user1",
            password=HASHED_PASSWORD,
            salt=SALT,
            createdAt=datetime.now(),
            lastEdited=datetime.now(),
        )) 

        # When
        result = _security.basic_auth(username="user1", password=PASSWORD)

        # Then
        assert isinstance(result, dict)
    def test_password_not_matches(self, put_users_table, session, mock_engine):
        """Given that I have a users table
        And that table contains one user "user1"
        When I authenticate user "user1"
        And I use the correct password
        Then None is returned
        """
        # Given
        SALT = "salt1"
        PASSWORD = "abc123"
        HASHED_PASSWORD = sha3_512((SALT + PASSWORD).encode("utf-8")).hexdigest()
        _user._postOne(session, _user.User(
            name="user1",
            password=HASHED_PASSWORD,
            salt=SALT,
            createdAt=datetime.now(),
            lastEdited=datetime.now(),
        )) 

        # When
        result = _security.basic_auth(username="user1", password="something_else")

        # Then
        assert result is None
