from typing import Optional, List
import os
from datetime import datetime

from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, Session
from sqlalchemy import select
from sqlalchemy.orm import mapped_column
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

class _Base(DeclarativeBase):
    pass

class User(_Base):
    __tablename__ = "users"

    _id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(128))
    salt: Mapped[str] = mapped_column(String(50))
    createdAt: Mapped[datetime] = mapped_column(DateTime)
    lastEdited: Mapped[datetime] = mapped_column(DateTime)
    
    def __repr__(self):
        pairs = "; ".join(f"{k}: {v}" for k,v in self.__dict__.items() if k != "_sa_instance_state")
        return f"User({pairs})"

def getOne(session: Session, **by) -> User:
    """Get a user from the database.

    * If one user match, return that user.
    * Otherwise, raise.

    Raises
    ------
    NoResultFound
        No users match.
    MultipleResultsFound
        Multiple users match.

    Parameters
    ----------
    session: Session
        Database session.
    by
        Keyword arguments used to filter for a specific user.
    
    Returns
    -------
    User
        A user in the table.
    """
    return session.execute(select(User).filter_by(**by)).scalar_one()

def _postOne(session: Session, user: User) -> None:
    """Add a user to the database.

    Raises
    ------
    IntegrityError
        User cannot be added to the database, due to an integrity problem
        (constraint violation, et cetera).

    Parameters
    ----------
    session: Session
        Database session.
    user: User
        A user to add to the table.
    """
    session.add(user)
    session.commit()

    return
