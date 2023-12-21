import pytest
from datetime import datetime
import os

from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

from api.v0.utils.security import _user

@pytest.fixture(scope="module")
def engine():
    return create_engine("sqlite+pysqlite:///:memory:", echo=True)

@pytest.fixture(scope="module")
def metadata(engine):
    return MetaData()

@pytest.fixture(scope="module")
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

class Test__getOne:
    def test_empty_table(self, put_users_table, session):
        """Given that I have a users table
        And that table is empty
        When I look for user with name "user1"
        Then NoResultFound is raised
        """
        with pytest.raises(NoResultFound):
            _user.getOne(session, name="user1")
    def test_no_user(self, put_users_table, session):
        """Given that I have an empty users table
        And that table contains one user "user1"
        When I look for user with name "user2"
        Then NoResultFound is raised
        """
        # Given
        _user._postOne(session, _user.User(
            name="user1",
            password="password1",
            salt="salt1",
            createdAt=datetime.now(),
            lastEdited=datetime.now(),
        )) 

        with pytest.raises(NoResultFound):
            # When; Then
            _user.getOne(session, name="user2")
    def test_one_user(self, put_users_table, session):
        """Given that I have an empty users table
        And that table contains one user "user1"
        When I look for user with name "user1"
        Then I get User "user1"
        """
        # Given
        user = _user.User(
            name="user1",
            password="password1",
            salt="salt1",
            createdAt=datetime.now(),
            lastEdited=datetime.now(),
        )
        _user._postOne(session, user) 

        # When
        result = _user.getOne(session, name="user1")

        # Then
        assert result == user
    def test_two_users(self, put_users_table, session):
        """Given that I have an empty users table
        And that table contains one user "user1" with password "abc123"
        And that table contains one user "user2" with password "abc123"
        When I look for user with password "abc123"
        Then MultipleResultsFound is raised
        """
        # Given
        _user._postOne(session, _user.User(
            name="user1",
            password="abc123",
            salt="salt1",
            createdAt=datetime.now(),
            lastEdited=datetime.now(),
        )) 
        _user._postOne(session, _user.User(
            name="user2",
            password="abc123",
            salt="salt2",
            createdAt=datetime.now(),
            lastEdited=datetime.now(),
        )) 

        with pytest.raises(MultipleResultsFound):
            # When; Then
            _user.getOne(session, password="abc123")
