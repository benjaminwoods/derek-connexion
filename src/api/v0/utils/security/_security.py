from typing import TypedDict
import os

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from hashlib import sha3_512

from ._user import getOne, User

if os.getenv("SQLALCHEMY_URL"):
    engine = create_engine(os.getenv("SQLALCHEMY_URL"))
else:
    engine = None

class _UserIdentity(TypedDict):
    pass

def basic_auth(username: str, password: str, required_scopes: None = None):
    """Authenticate a user.

    Checks if a user is recognized as a registered user. This function
    does not check if the user is authorized to use any functionality.

    Notes
    -----
    Basic auth does not yet support scoped access. As a result, required_scopes
    currently must be None.

    Parameters
    ----------
    username: str
        Username.
    password: str
        Pre-hash password.
    required_scopes: None
        An optional list of scopes.

        Currently, this must be None.

    Returns
    -------
    dict
        User identity.

        This user identity is RFC 7662 compliant.
    """
    with Session(engine) as session:
        try:
            # Grab user
            u = session.execute(select(User).filter_by(name=username)).scalar_one()
        except (NoResultFound, MultipleResultsFound):
            # No user found
            return None
        
        # Hash password
        plaintext = (u.salt + password).encode("utf-8")
        hashed_password = sha3_512(plaintext).hexdigest()

        if hashed_password == u.password:
            # Return the user identity
            return _UserIdentity()
        else:
            # Password does not match
            return None

def api_key(*args, **kwargs):
    return {}