#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""database models"""

import base64
import typing as t
from datetime import datetime
from enum import Enum, auto
from secrets import SystemRandom

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from sqlalchemy import Enum as StorageEnum
from sqlalchemy import Unicode, or_

from . import const

db: SQLAlchemy = SQLAlchemy()

rand: SystemRandom = SystemRandom()

limiter: Limiter = Limiter(
    get_remote_address,
    storage_uri="memcached://127.0.0.1:18391",
    strategy="fixed-window",
)


class AccessLevel(Enum):
    """access level of an access token"""

    write = auto()
    admin = auto()


class AccessKey(db.Model):
    """access key"""

    key: str = db.Column(
        db.String(const.KEY_LEN),
        unique=True,
        nullable=False,
        primary_key=True,
    )
    access_level: AccessLevel = db.Column(
        StorageEnum(
            AccessLevel,
            default=AccessLevel.write,
        )
    )

    def __init__(self, acceess_level: AccessLevel = AccessLevel.write) -> None:
        """create a new access key"""

        self.access_level: AccessLevel = acceess_level

        while True:
            key: str = base64.urlsafe_b64encode(
                rand.randbytes(const.KEY_LEN * 2)
            ).decode()[: const.KEY_LEN]

            if self.query.filter_by(key=key).first() is None:
                self.key = key
                break

    def json(self) -> t.Dict[str, t.Any]:
        """return json"""

        return {
            "key": self.key,
            "access": self.access_level.name,
        }


class Image(db.Model):
    """image"""

    iid: int = db.Column(
        db.Integer,
        primary_key=True,
        unique=True,
    )
    desc: t.Optional[str] = db.Column(Unicode(const.DESC_LEN))
    created: datetime = db.Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    edited: datetime = db.Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    score: int = db.Column(
        db.Integer,
        default=0,
    )

    def __init__(self, desc: t.Optional[str] = None) -> None:
        """create a new image"""
        self.set_desc(desc)

    # i just dislike properties for db stuff

    def set_desc(self, desc: t.Optional[str] = None) -> "Image":
        """set `desc` description"""

        if desc:
            assert len(desc) <= const.DESC_LEN, "description too long"

        self.desc: t.Optional[str] = desc
        return self

    def json(self) -> t.Dict[str, t.Any]:
        """return json"""

        return {
            "iid": self.iid,
            "desc": self.desc,
            "created": self.created.timestamp(),
            "edited": self.edited.timestamp(),
            "score": self.score,
        }

    @classmethod
    def by_search(cls, query: str) -> t.Tuple["Image", ...]:
        """search for images"""

        query = query.lower()

        return tuple(
            cls.query.filter(
                or_(
                    cls.desc.ilike(f"%{query}%"),  # type: ignore
                    cls.created.cast(db.String).ilike(f"%{query}%"),  # type: ignore
                    cls.edited.cast(db.String).ilike(f"%{query}%"),  # type: ignore
                    cls.score.cast(db.String).ilike(f"%{query}%"),  # type: ignore
                )
            )
            .order_by(cls.created.desc())  # type: ignore
            .order_by(cls.score.desc())  # type: ignore
            .all()
        )
